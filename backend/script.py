import os
import asyncio
import asyncpg

async def main():
	conn = await asyncpg.connect(
		user=os.getenv("USER"),
		password=os.getenv("PASSWORD"),
		database=os.getenv("DB"),
		host=os.getenv("HOST"),
		port=os.getenv("DB_PORT")
	)
	
	print(os.getenv("USER"))

	await conn.execute("""
		CREATE TABLE IF NOT EXISTS fake3 (
			id SERIAL PRIMARY KEY,
			name VARCHAR(50) NOT NULL
		)
	""")

	await conn.execute("INSERT INTO fake3 (name) VALUES ($1)", "Alfred")

	rows = await conn.fetch("SELECT * FROM fake3")
	for row in rows:
		print(dict(row))

	rows = await conn.fetch("SELECT * FROM fake2")
	for row in rows:
		print(dict(row))  

	await conn.close()

if __name__ == "__main__":
	asyncio.run(main())