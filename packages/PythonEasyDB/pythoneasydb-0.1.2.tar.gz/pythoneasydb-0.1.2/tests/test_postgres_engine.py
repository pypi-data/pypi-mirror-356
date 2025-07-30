# tests/test_postgres_engine.py

import os
import pytest
from PythonEasyDB.engines.postgres_engine import PostgresEngine

PG_URI = os.getenv("POSTGRES_URI", "postgresql://postgres:postgres@localhost:5432/unidb_test")

def setup_module(module):
    db = PostgresEngine(PG_URI)
    db.cursor.execute("DROP TABLE IF EXISTS users")
    db.conn.commit()
    db.close()

def test_postgres_crud_operations():
    db = PostgresEngine(PG_URI)
    
    db.create_table(
        "users",
        id={"type": "int", "primary_key": True, "auto_increment": True},
        name="str",
        age="int",
        status={"type": "str", "default": "active"},
        is_admin={"type": "bool", "default": False},
    )

    db.insert("users", {"id": 1, "name": "Ali", "age": 17})
    db.insert("users", {"id": 2, "name": "Vali", "age": 21, "is_admin": True})
    db.insert("users", {"id": 3, "name": "Dali", "age": 18, "status": "inactive"})

    results = db.select("users")
    assert len(results) == 3

    active_users = db.select("users", where={"status": "active"})
    assert len(active_users) == 2

    db.update("users", where={"age__lt": 18}, values={"status": "minor"})
    minors = db.select("users", where={"status": "minor"})
    assert len(minors) == 1
    # assert minors[0][1] == "Ali"

    db.delete("users", where={"age__gt": 20})
    remaining = db.select("users")
    assert len(remaining) == 2

    db.close()
