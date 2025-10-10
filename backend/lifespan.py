import os
import ssl
from contextlib import asynccontextmanager
#import aioredis

from fastapi import FastAPI
from tortoise import Tortoise


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(
        db_url=f"postgres://{os.getenv("user")}:{os.getenv("password")}@localhost:5432/keiser",
        modules={"models": ["app.models"]}
    )
    
    await Tortoise.generate_schemas()
    
    #app.state.redis = await aioredis.from_url(
    #    "redis://localhost:6739",
    #    decode_responses=True    
    #)

    try: 
        yield
    finally:
        await app.state.redis.close()
        await Tortoise.close_connections()
    
