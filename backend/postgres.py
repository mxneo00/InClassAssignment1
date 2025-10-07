import os

import asyncpg

# Database connection parameters retrieved from environment variables
db_config = {
    "host": "",
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "db": os.getenv("DB"),
    "port": os.getenv("PORT"),
}

class PostgresAdapter:
    def __init__(self) -> None:
        self.pool = None

    async def create_pool(self, db_params: dict) -> None:
        try:
            self.pool = await asyncpg.create_pool(**db_params)
            # logger.info("PostgreSQL connection pool created successfully")
        except Exception as e:
            raise ValueError(f"Failed to create connection pool: {e}") from e

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
            # logger.info("PostgreSQL connection pool closed")

    async def inject(self, base_path: str) -> None:
        try:
            schema = os.getenv("DB_SCHEMA", "") + base_path
            if not os.path.exists(schema):
                raise ValueError("Schema file not found!")

            with open(schema) as f:
                byte_str = f.read()

            async with self.pool.acquire() as conn:
                await conn.execute(byte_str)
            # logger.info("Schema loaded successfully.")
        except Exception as e:
            # logger.info(f"Error: {e}")
            pass

    async def insert(self, table: str, record: dict[str, any]) -> None:
        columns = ", ".join(record.keys())
        values = ", ".join(
            ["$" + str(i + 1) for i in range(len(record))]
        )  # Placeholder for parameterized query
        sql_query = f'INSERT INTO "{table}" ({columns}) VALUES ({values})'

        try:
            async with self.pool.acquire() as conn:
                await conn.execute(
                    sql_query, *list(record.values())
                )  # Execute with parameters
            # logger.info("Record inserted successfully.")
        except Exception as e:
            raise ValueError(f"Error inserting record: {e}") from e

    async def all(self, table: str) -> list[dict[str, any]]:
        sql_query = f"SELECT * FROM {table};"
        async with self.pool.acquire() as conn:
            records = await conn.fetch(sql_query)

        # Convert to a list of dictionaries
        columns = [desc["name"] for desc in conn.description]
        results = [dict(zip(columns, record, strict=False)) for record in records]

        return results

    async def tables(self) -> list[str]:
        async with self.pool.acquire() as conn:
            vals = await conn.fetch(
                "SELECT schemaname, relname FROM pg_stat_user_tables;"
            )

        tables = [val[1] for val in vals]  # Collect table names
        # logger.info("TABLES: ")
        for table in tables:
            pass
            # logger.info(f"\t{table}")
        return tables

    async def update(
        self, json: dict[str, any], condition: str, condition_val: str
    ) -> None:
        async with self.pool.acquire() as conn:
            for table, record in json.items():
                attrs = record.keys()
                set_clause = ", ".join(
                    [f"{attr} = ${i + 1}" for i, attr in enumerate(attrs)]
                )
                values = list(record.values())
                table_name = table

                update_query = f"""
                    UPDATE {table_name} SET {set_clause}
                    WHERE {condition} = ${{{len(values) + 1}}}
                """

                try:
                    await conn.execute(update_query, *values, condition_val)
                    # logger.info(f"Update on '{table}' successful")
                except Exception as e:
                    pass
                    # logger.info(f"Failed to update record in table '{table}': {e}")

    async def exec(self, query: str) -> None:
        try:
            async with self.pool.acquire() as conn:
                result = await conn.fetch(query)
            return result
        except Exception as e:
            # logger.info(f"Failed to execute query: {e}")
            raise OSError(f"Failed to execute query: {e}") from e

    async def attrs(self, table_name: str) -> list[str]:
        async with self.pool.acquire() as conn:
            column_names = await conn.fetch(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name='{table_name}'
            """)

        column_names = [row["column_name"] for row in column_names]
        # logger.info("Column Names: ", column_names)
        return column_names

    async def find_by(self, table_: str, attr_: str, val: any) -> list[dict[str, any]]:
        table = table_
        attr = attr_
        query = f"SELECT * FROM {table} WHERE {attr} = $1"

        async with self.pool.acquire() as conn:
            result = await conn.fetch(query, val)

        # Convert results to a list of dictionaries
        columns = [desc["name"] for desc in conn.description]
        records = [dict(zip(columns, record, strict=False)) for record in result]

        return records
