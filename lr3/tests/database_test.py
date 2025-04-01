import os
import tempfile

import pytest
from database.database import Database, DepartmentTable, EmployeeTable, GoodsTable


@pytest.fixture
def temp_files():
    temp_files = {
        "employees": tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name,
        "departments": tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name,
        "goods": tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name,
    }
    yield temp_files
    for file in temp_files.values():
        os.remove(file)


@pytest.fixture
def database(temp_files):
    db = Database()

    employee_table = EmployeeTable()
    employee_table.FILE_PATH = temp_files["employees"]
    department_table = DepartmentTable()
    department_table.FILE_PATH = temp_files["departments"]
    goods_table = GoodsTable()
    goods_table.FILE_PATH = temp_files["goods"]

    db.register_table("employees", employee_table)
    db.register_table("departments", department_table)
    db.register_table("goods", goods_table)

    return db


@pytest.fixture
def temp_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    temp_file.close()
    yield temp_file.name
    os.remove(temp_file.name)


def test_load_employee_table(temp_file):
    data = "id,name,age,salary,department_id\n1,Alice,30,70000,10\n2,Bob,28,60000,20\n"
    with open(temp_file, "w") as f:
        f.write(data)

    table = EmployeeTable()
    table.FILE_PATH = temp_file
    table.load()

    assert len(table.data) == 2
    assert table.data[0]["id"] == "1"
    assert table.data[1]["id"] == "2"
    assert ("1", "10") in table.unique_keys


def test_load_department_table(temp_file):
    data = "id,department_name\n10,HR\n20,Engineering\n"
    with open(temp_file, "w") as f:
        f.write(data)

    table = DepartmentTable()
    table.FILE_PATH = temp_file
    table.load()

    assert len(table.data) == 2
    assert table.data[0]["id"] == "10"
    assert table.data[1]["id"] == "20"
    assert "10" in table.unique_keys


def test_load_goods_table(temp_file):
    data = "id,name,price,department_id\n100,Laptop,1500,20\n200,Mouse,50,10\n"
    with open(temp_file, "w") as f:
        f.write(data)

    table = GoodsTable()
    table.FILE_PATH = temp_file
    table.load()

    assert len(table.data) == 2
    assert table.data[0]["id"] == "100"
    assert table.data[1]["id"] == "200"


def test_insert_employee(database):
    database.insert("employees", "1 Alice 30 70000 101")
    database.insert("employees", "2 Bob 28 60000 102")
    employee_data = database.select("employees", 1, 2)
    assert len(employee_data) == 2
    assert employee_data[0]["name"] == "Alice"
    assert employee_data[1]["name"] == "Bob"
    with pytest.raises(ValueError):
        database.insert("justtable", "1 asd 123")


def test_unique_employee(database):
    database.insert("employees", "1 Alice 30 70000 101")
    with pytest.raises(ValueError):
        database.insert("employees", "1 Alice 30 70000 101")


def test_insert_department(database):
    database.insert("departments", "101 HR")
    database.insert("departments", "102 IT")
    department_data = database.select("departments", "HR")
    assert len(department_data) == 1
    assert department_data[0]["department_name"] == "HR"


def test_unique_department(database):
    database.insert("departments", "101 HR")
    with pytest.raises(ValueError):
        database.insert("departments", "101 HR")


def test_insert_goods(database):
    database.insert("goods", "1 Laptop 1200 101")
    database.insert("goods", "2 Mouse 50 101")
    database.insert("goods", "3 Keyboard 80 102")
    good_data = database.select("goods", 60, 100)
    assert len(good_data) == 1
    assert good_data[0]["name"] == "Keyboard"


def test_join(database):
    database.insert("departments", "101 HR")
    database.insert("departments", "102 IT")
    database.insert("employees", "1 Alice 30 70000 101")
    database.insert("employees", "2 Bob 28 60000 102")
    result = database.join(
        [database.tables["employees"], database.tables["departments"]],
        [("department_id", "id")],
    )
    assert len(result) == 2
    assert result[0]["department_name"] == "HR"
    assert result[1]["department_name"] == "IT"
    with pytest.raises(ValueError):
        result = database.join(
            [database.tables["employees"]], [("department_id", "id")]
        )


def test_aggregate(database):
    db = database
    db.insert("goods", "100 Laptop 1500 20")
    db.insert("goods", "200 Mouse 50 10")
    db.insert("goods", "300 Keyboard 100 10")

    assert db.aggregate("goods", "count", "price") == 3
    assert db.aggregate("goods", "avg", "price") == 550.0

    with pytest.raises(ValueError):
        db.aggregate("justtable", "count", "price")
    with pytest.raises(ValueError):
        db.aggregate("goods", "avg", "name")
