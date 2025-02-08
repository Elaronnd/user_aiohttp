import asyncio
import aiomysql
import aiohttp

loop = asyncio.get_event_loop()
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'SleepHat',
    'db': 'users',
    'autocommit': True,
}


async def add_user_to_db(
        user: str,
        password: str,
):
    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cur:
        sql_query = "INSERT INTO books (user, password) VALUES (%s, %s)"
        await cur.execute(sql_query, (user, password))

        await cur.close()

    conn.close()
    return True


async def get_user_from_db(
        user: str,
):
    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cur:
        sql_query = f"SELECT * FROM users WHERE user = {user}"
        await cur.execute(sql_query)
        book = await cur.fetchone()

    conn.close()
    return book


async def delete_user_from_db(
        user: int,
        password: str
):
    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cur:
        sql_query = f"DELETE FROM users WHERE user = {user} AND password = {password}"
        await cur.execute(sql_query)

        if cur.rowcount == 0:
            conn.close()
            return [False, "No matching user found"]

    conn.close()
    return [True, "deleted"]
