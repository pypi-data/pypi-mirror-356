# unidb/engines/redis_engine.py

import redis
import json
from PythonEasyDB.utils import DBError
from urllib.parse import urlparse

class RedisEngine:
    def __init__(self, uri):

        try:
            if not uri.startswith("redis://"):
                raise ValueError("Redis URI must start with 'redis://'")

            parsed = urlparse(uri)
            host = parsed.hostname or "localhost"
            port = parsed.port or 6379
            db = int(parsed.path.lstrip('/')) if parsed.path else 0

            self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            self.client.ping()
        except Exception as e:
            raise DBError(f"Could not connect to Redis: {e}")

    def set(self, key, value):
        try:
            value_str = json.dumps(value)
            self.client.set(key, value_str)
        except Exception as e:
            raise DBError(f"Failed to set key '{key}': {e}")

    def get(self, key):
        try:
            val = self.client.get(key)
            return json.loads(val) if val else None #type: ignore
        except Exception as e:
            raise DBError(f"Failed to get key '{key}': {e}")

    def delete(self, key):
        try:
            return self.client.delete(key)
        except Exception as e:
            raise DBError(f"Failed to delete key '{key}': {e}")

    def exists(self, key):
        try:
            return self.client.exists(key) == 1
        except Exception as e:
            raise DBError(f"Failed to check existence of key '{key}': {e}")

    def keys(self, pattern="*"):
        try:
            return self.client.keys(pattern)
        except Exception as e:
            raise DBError(f"Failed to retrieve keys: {e}")

    def flush(self):
        try:
            self.client.flushdb()
        except Exception as e:
            raise DBError(f"Failed to flush database: {e}")

    def close(self):
        try:
            self.client.close()
        except Exception as e:
            raise DBError(f"Failed to close Redis connection: {e}")
