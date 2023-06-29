import asyncpg
import pytest_asyncio
from config import POSTGRES_URL


@pytest_asyncio.fixture
async def conn() -> asyncpg.Connection:
    try:
        conn = await asyncpg.connect(POSTGRES_URL)
        return conn
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")


@pytest_asyncio.fixture
async def create_db(conn) -> None:
    # Создаем таблицу из задания
    await conn.execute(
        """CREATE TABLE IF NOT EXISTS People (
            Index SERIAL PRIMARY KEY,
            FirstName TEXT,
            FamilyName TEXT,
            DateOfBirth DATE,
            PlaceOfBirth TEXT,
            Occupation TEXT,
            Hubby TEXT
        );"""
        )
    
    yield
    # Удаляем таблицу, если не произошло переименования
    await conn.execute(f"DROP TABLE IF EXISTS People;")
    # Закрываем соединение
    await conn.close()
    