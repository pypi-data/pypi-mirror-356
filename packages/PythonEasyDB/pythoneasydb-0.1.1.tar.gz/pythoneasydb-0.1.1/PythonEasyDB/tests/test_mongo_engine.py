# tests/test_mongo_engine.py

import pytest
from PythonEasyDB.engines.mongo_engine import MongoEngine

MONGO_URI = "mongodb://asrorbekaliqulov08:<db_password>@cluster0.tfjy0.mongodb.net/unidb_test?retryWrites=true&w=majority&authSource=admin&cluster=atlas"

def setup_module(module):
    db = MongoEngine(MONGO_URI)
    db.db.drop_collection("users")
    db.close()

def test_mongo_crud_operations():
    db = MongoEngine(MONGO_URI)

    db.create_table("users")  # MongoDB'da bu faqat collection yaratadi

    db.insert("users", {"name": "Ali", "age": 17})
    db.insert("users", {"name": "Vali", "age": 21, "is_admin": True})
    db.insert("users", {"name": "Dali", "age": 18, "status": "inactive"})

    all_users = db.select("users")
    assert len(all_users) == 3

    active = db.select("users", where={"status": "active"})
    assert len(active) == 1 or len(active) == 0  # default ishlashi ixtiyoriy bo'lishi mumkin

    db.update("users", where={"age__lt": 18}, values={"status": "minor"})
    minors = db.select("users", where={"status": "minor"})
    assert len(minors) == 1

    db.delete("users", where={"age__gt": 20})
    remaining = db.select("users")
    assert len(remaining) == 2

    db.close()
