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
        # "discriptions" - описание теста
        [
            ### ПОЗИТИВНЫЕ ТЕСТЫ
            # тест №1
            {
                "table_name": "newname",
                "result": True,
                "discriptions": "переименование таблицы, используя латиницу",
            },
            # тест №2
            {
                "table_name": "таблица1",
                "result": True,
                "discriptions": "переименование таблицы, используя кирилицу",
            },
            # тест №3
            {
                "table_name": "newname ",
                "result": True,
                "discriptions": "переименование таблицы, в конце пробел",
            },
            # тест №4
            {
                "table_name": " newname",
                "result": True,
                "discriptions": "переименование таблицы, вначале пробел",
            },
            # тест №5
            {
                "table_name": " newname ",
                "result": True,
                "discriptions": "переименование таблицы, вначале и в конце пробел",
            },
            # тест №6
            {
                "table_name": '"newname 2"',
                "result": True,
                "discriptions": "переименование таблицы, название таблицы из 2х слов",
            },
            # тест №7
            {
                "table_name": '" newname 2"',
                "result": True,
                "discriptions": "переименование таблицы, название из 2х слов, пробел вначале",
            },
            # тест №8
            {
                "table_name": '"newname 2 "',
                "result": True,
                "discriptions": "переименование таблицы, название таблицы из 2х слов, пробел вконце",
            },
            # тест №9
            {
                "table_name": '" newname 2 "',
                "result": True,
                "discriptions": "переименование таблицы, название из 2х слов, пробел вначале и вконце",
            },
            # тест №10
            {
                "table_name": "this_is_a_table_with_63_characters_in_its_name_contains_number",
                "result": True,
                "discriptions": "переименование таблицы, 62 символа в названии",
            },
            # тест №11
            {
                "table_name": "this_is_a_table_with_63_characters_in_its_name_contains_numbers",
                "result": True,
                "discriptions": "переименование таблицы, 63 символа в названии",
            },
            ### НЕГАТИВНЫЕ ТЕСТЫ
            # тест №12
            {
                "table_name": "",
                "result": False,
                "discriptions": "переименование таблицы, пустое название",
            },
            # тест №13
            {
                "table_name": "1newname",
                "result": False,
                "discriptions": "переименование таблицы, название начинается с цифры",
            },
            # тест №14
            {
                "table_name": "newname%",
                "result": False,
                "discriptions": "переименование таблицы, название недопустимые символы",
            },
            # тест №15
            {
                "table_name": "new name",
                "result": False,
                "discriptions": "переименование таблицы, из 2х слов, без использования кавычек",
            },
            # тест №16
            {
                "table_name": "this_is_a_table_with_63_characters_in_its_name_contains_numbers_",
                "result": False,
                "discriptions": "переименование таблицы, 64 символа в назнании",
            },
            # тест №17
            {
                "table_name": "People",
                "result": False,
                "discriptions": "переименование таблицы, на существующее название",
            },
        ]
    ),
)
@allure.feature("Тестирование изменения таблицы")
# @allure.title("Изменение названия таблицы")
@allure.severity("blocker")
async def test_rename_table(create_db, conn, param) -> None:
    """
    Тесты переименования таблицы People
    """
    table_name = param["table_name"].strip().replace('"', "")

    rename_query = f"ALTER TABLE People RENAME TO {param['table_name']};"

    fetch_query = (
        "SELECT table_name FROM information_schema.tables WHERE table_name = $1"
    )

    drop_query = f"DROP TABLE IF EXISTS {param['table_name']};"

    try:
        await conn.execute(rename_query)
    except:
        assert param["result"] == False, "Название таблицы невалидное"
    else:
        result = await conn.fetchval(fetch_query, table_name[:63])
        if len(table_name) <= 63:
            assert (
                result == table_name[:63] and param["result"]
            ), "Таблица не переименовалась"
        else:
            assert len(result) == 63, "Название наблицы не может быть более 63 символов"

        # Удаляем переименованную таблицу
        await conn.execute(drop_query)
