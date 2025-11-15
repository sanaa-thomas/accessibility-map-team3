import aiomysql # type: ignore
import asyncio
import os

async def get_db_pool():
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "2005")
    db = os.getenv("DB_NAME", "campus_map")
    return await aiomysql.create_pool(
        host=host,
        port=port,
        user=user,
        password=password,
        db=db,
        autocommit=True,
        #host="localhost",
        #port=3306,
        #user="root",
        #password="2005",
        # db="campus_map",
        #autocommit=True
    )
