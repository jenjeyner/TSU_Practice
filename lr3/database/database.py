import csv
import os
from abc import ABC, abstractmethod


class SingletonMeta(type):
    """Синглтон метакласс для Database."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """Класс-синглтон базы данных с таблицами, хранящимися в файлах."""

    def __init__(self):
        self.tables = {}

    def register_table(self, table_name, table):
        self.tables[table_name] = table

    def insert(self, table_name, data):
        table = self.tables.get(table_name)
        if table:
            table.insert(data)
        else:
            raise ValueError(f"Table {table_name} does not exist.")

    def select(self, table_name, *args):
        table = self.tables.get(table_name)
        return table.select(*args) if table else None

    def join(self, tables, join_attrs):
        """Универсальный метод JOIN для объединения нескольких таблиц
        по заданным атрибутам."""
        if len(tables) < 2:
            raise ValueError("JOIN requires at least two tables.")

        joined_data = tables[0].data
        for i in range(1, len(tables)):
            table = tables[i]
            attr1, attr2 = join_attrs[i - 1]
            joined_data = [
                {**row1, **row2}
                for row1 in joined_data
                for row2 in table.data
                if row1.get(attr1) == row2.get(attr2)
            ]
        return joined_data

    def aggregate(self, table_name, operation, field):
        table = self.tables.get(table_name)
        if not table:
            raise ValueError("Table does not exist.")

        values = [row[field] for row in table.data if field in row]

        if operation == "avg":
            try:
                numeric_values = list(map(float, values))
            except ValueError:
                raise ValueError("Cannot calculate average for non-numeric values.")
            return sum(numeric_values) / len(numeric_values)

        operations = {"min": min(values), "max": max(values), "count": len(values)}
        return operations.get(operation, f"Unknown aggregation method '{operation}'")


class Table(ABC):
    """Абстрактный базовый класс для таблиц с вводом/выводом файлов CSV."""

    @abstractmethod
    def insert(self, data):  # pragma: no cover
        pass

    @abstractmethod
    def select(self, *args):  # pragma: no cover
        pass


class EmployeeTable(Table):
    ATTRS = ("id", "name", "age", "salary", "department_id")
    FILE_PATH = "employee_table.csv"

    def __init__(self):
        self.data = []
        self.unique_keys = set()
        self.load()

    def insert(self, data):
        entry = dict(zip(self.ATTRS, data.split()))
        key = (entry["id"], entry["department_id"])
        if key in self.unique_keys:
            raise ValueError("Duplicate (id, department_id) found.")
        self.data.append(entry)
        self.unique_keys.add(key)
        self.save()

    def select(self, start_id, end_id):
        return [entry for entry in self.data if start_id <= int(entry["id"]) <= end_id]

    def save(self):
        with open(self.FILE_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.ATTRS)
            writer.writeheader()
            writer.writerows(self.data)

    def load(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r") as f:
                reader = csv.DictReader(f)
                self.data = [row for row in reader]
                self.unique_keys = {
                    (row["id"], row["department_id"]) for row in self.data
                }
        else:
            self.data = []


class DepartmentTable(Table):
    ATTRS = ("id", "department_name")
    FILE_PATH = "department_table.csv"

    def __init__(self):
        self.data = []
        self.unique_keys = set()
        self.load()

    def insert(self, data):
        entry = dict(zip(self.ATTRS, data.split()))
        if entry["id"] in self.unique_keys:
            raise ValueError("Duplicate department_id found.")
        self.data.append(entry)
        self.unique_keys.add(entry["id"])
        self.save()

    def select(self, department_name):
        return [
            entry for entry in self.data if entry["department_name"] == department_name
        ]

    def save(self):
        with open(self.FILE_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.ATTRS)
            writer.writeheader()
            writer.writerows(self.data)

    def load(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r") as f:
                reader = csv.DictReader(f)
                self.data = [row for row in reader]
                self.unique_keys = {row["id"] for row in self.data}
        else:
            self.data = []


class GoodsTable(Table):
    ATTRS = ("id", "name", "price", "department_id")
    FILE_PATH = "goods_table.csv"

    def __init__(self):
        self.data = []
        self.load()

    def insert(self, data):
        entry = dict(zip(self.ATTRS, data.split()))
        self.data.append(entry)
        self.save()

    def select(self, min_price, max_price):
        return [
            entry
            for entry in self.data
            if min_price <= float(entry["price"]) <= max_price
        ]

    def save(self):
        with open(self.FILE_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.ATTRS)
            writer.writeheader()
            writer.writerows(self.data)

    def load(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r") as f:
                reader = csv.DictReader(f)
                self.data = [row for row in reader]
        else:
            self.data = []
