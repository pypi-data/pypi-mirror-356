# tests/test_redis_engine.py

import pytest
from PythonEasyDB.engines.redis_engine import RedisEngine

REDIS_URI = "redis://localhost:6379/1"

def setup_module(module):
    db = RedisEngine(REDIS_URI)
    db.flush()
    db.close()

def test_redis_operations():
    db = RedisEngine(REDIS_URI)

    db.set("user:1", {"name": "Ali", "age": 17})
    db.set("user:2", {"name": "Vali", "age": 21})

    val1 = db.get("user:1")
    assert val1["name"] == "Ali"

    all_keys = db.keys("user:*")
    assert len(all_keys) == 2

    assert db.exists("user:1")
    db.delete("user:1")
    assert not db.exists("user:1")

    db.close()
