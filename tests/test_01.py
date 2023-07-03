import sys
import pytest
import pytest_asyncio
import allure


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "param",
    (
        # "table_name" - название таблицы
        # "result" - ожидаемый результат переименования
        [
            ### ПОЗИТИВНЫЕ ТЕСТЫ
            # переименование используя латиницу
            {"table_name": "newname", "result": True},
            # переименование используя кирилицу
            {"table_name": "таблица1", "result": True},
            # переименование вконце пробел
            {"table_name": "newname ", "result": True},
            # переименование вначале пробел
            {"table_name": " newname", "result": True},
            # переименование вначале и в конце пробел
            {"table_name": " newname ", "result": True},
            # переименование, название таблицы из 2х слов
            {"table_name": '"newname 2"', "result": True},
            # переименование, название таблицы из 2х слов, пробел вначале
            {"table_name": '" newname 2"', "result": True},
            # переименование, название таблицы из 2х слов, пробел вконце
            {"table_name": '"newname 2 "', "result": True},
            # переименование, название таблицы из 2х слов, пробел вначале и вконце
            {"table_name": '" newname 2 "', "result": True},
            # 62 символа в назнании
            {
                "table_name": "this_is_a_table_with_63_characters_in_its_name_contains_number",
                "result": True,
            },
            # 63 символа в назнании
            {
                "table_name": "this_is_a_table_with_63_characters_in_its_name_contains_numbers",
                "result": True,
            },
            ### НЕГАТИВНЫЕ ТЕСТЫ
            # переименование пустое название
            {"table_name": "", "result": False},
            # переименование название начинается с цифры
            {"table_name": "1newname", "result": False},
            # переименование название недопустимые символы
            {"table_name": "newname%", "result": False},
            # переименование из 2х слов, без использования кавычек
            {"table_name": "new name", "result": False},
            # 64 символа в назнании
            {
                "table_name": "this_is_a_table_with_63_characters_in_its_name_contains_numbers_",
                "result": False,
            },
        ]
    ),
)
@allure.feature("1) Изменение названия")
@allure.title("Позитивные тесты")
@allure.severity("blocker")
async def test_rename_table(create_db, conn, param) -> None:
    f"""{param['table_name']}"""
    try:
        await conn.execute(f"ALTER TABLE People RENAME TO {param['table_name']};")
    except:
        assert param["result"] == False, "Название таблицы невалидное"
    else:
        result = await conn.fetchval(
            """SELECT table_name FROM information_schema.tables WHERE table_name = $1""",
            param["table_name"].strip().replace('"', "")[:63],
        )
        if len(param["table_name"].strip().replace('"', "")) <= 63:
            assert (
                result == param["table_name"].strip().replace('"', "")[:63]
                and param["result"]
            ), "Таблица не переименовалась"
        else:
            assert len(result) == 63, "Название наблицы не может быть более 63 символов"

        # Удаляем переименованную таблицу
        await conn.execute(f"""DROP TABLE IF EXISTS {param['table_name']};""")
