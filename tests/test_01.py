import sys
import pytest
import pytest_asyncio


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "param",
    (
        [
            # Позитивный тест (result - ожидаемый результат)
            {"table_name": "test1", "result": True},
            # Негативный тест (result - ожидаемый результат)
            {"table_name": "%!", "result": False},
        ]
    ),
)
async def test_rename(create_db, conn, param) -> None:
    try:
        await conn.execute(f"ALTER TABLE People RENAME TO {param['table_name']};")
    except:
        assert param["result"] == False, "Название таблицы невалидное"
    else:
        result = await conn.fetchval(
            "SELECT table_name FROM information_schema.tables WHERE table_name = $1",
            param["table_name"],
        )
        assert (
            result == param["table_name"] and param["result"]
        ), "Таблица не переименовалась"

        # Удаляем переименованную таблицу
        await conn.execute(f"DROP TABLE IF EXISTS {param['table_name']};")
