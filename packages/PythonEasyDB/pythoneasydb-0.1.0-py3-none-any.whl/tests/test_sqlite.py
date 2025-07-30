# tests/test_sqlite_engine.py

import os
import pytest
from PythonEasyDB.engines.sqlite_engine import SQLiteEngine

TEST_DB = "test_unidb.sqlite"

def setup_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def teardown_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_sqlite_crud_operations():
    db = SQLiteEngine(TEST_DB)

    db.create_table(
        "users",
        id={"type": "int", "primary_key": True, "auto_increment": True},
        name="str",
        age="int",
        status={"type": "str", "default": "active"},
        is_admin={"type": "bool", "default": False},
    )

    db.insert("users", {"name": "Ali", "age": 17})
    db.insert("users", {"name": "Vali", "age": 21, "is_admin": True})
    db.insert("users", {"name": "Dali", "age": 18, "status": "inactive"})

    results = db.select("users")
    assert len(results) == 3

    active_users = db.select("users", where={"status": "active"})
    assert len(active_users) == 2

    db.update("users", where={"age__lt": 18}, values={"status": "minor"})
    minors = db.select("users", where={"status": "minor"})
    assert len(minors) == 1
    assert minors[0][1] == "Ali"

    db.delete("users", where={"age__gt": 20})
    remaining = db.select("users")
    assert len(remaining) == 2
    print("Remaining users:", remaining)
    db.close()
