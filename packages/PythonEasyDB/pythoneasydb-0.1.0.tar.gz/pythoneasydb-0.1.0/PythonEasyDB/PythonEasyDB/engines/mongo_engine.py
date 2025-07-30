# unidb/engines/mongo_engine.py

from pymongo import MongoClient
from PythonEasyDB.utils import DBError
# from unidb.utils import parse_where  # Reuse if adapted for Mongo

class MongoEngine:
    def __init__(self, uri):
        try:
            if not uri.startswith("mongodb://"):
                raise ValueError("Mongo URI must start with 'mongodb://'")
            client = MongoClient(uri)
            self.db = client.get_default_database()
        except Exception as e:
            raise DBError(f"Could not connect to MongoDB: {e}")

    def create_table(self, collection_name, **kwargs):
        # MongoDB collections are created implicitly.
        try:
            self.db.create_collection(collection_name)
        except Exception as e:
            if "already exists" not in str(e):
                raise DBError(f"Could not create collection '{collection_name}': {e}")

    def insert(self, collection_name, document):
        try:
            return self.db[collection_name].insert_one(document).inserted_id
        except Exception as e:
            raise DBError(f"Insert failed for '{collection_name}': {e}")

    def select(self, collection_name, where=None, order_by=None, desc=False, limit=None, offset=None, group_by=None, having=None, distinct=False, joins=None):
        try:
            query = self._parse_where_mongo(where or {})
            cursor = self.db[collection_name].find(query)

            if order_by:
                direction = -1 if desc else 1
                cursor = cursor.sort(order_by, direction)

            if offset:
                cursor = cursor.skip(offset)
            if limit:
                cursor = cursor.limit(limit)

            return list(cursor)
        except Exception as e:
            raise DBError(f"Failed to select from '{collection_name}': {e}")

    def update(self, collection_name, where, updates):
        try:
            query = self._parse_where_mongo(where)
            result = self.db[collection_name].update_many(query, {"$set": updates})
            return result.modified_count
        except Exception as e:
            raise DBError(f"Failed to update '{collection_name}': {e}")

    def delete(self, collection_name, where):
        try:
            query = self._parse_where_mongo(where)
            result = self.db[collection_name].delete_many(query)
            return result.deleted_count
        except Exception as e:
            raise DBError(f"Failed to delete from '{collection_name}': {e}")

    def _parse_where_mongo(self, where):
        ops = {
            "lt": "$lt",
            "lte": "$lte",
            "gt": "$gt",
            "gte": "$gte",
            "ne": "$ne",
            "eq": None,
            "in": "$in",
            "notin": "$nin",
            "exists": "$exists",
            "regex": "$regex"
        }
        
        mongo_query = {}

        for key, val in where.items():
            if "__" in key:
                field, op = key.split("__", 1)
                mongo_op = ops.get(op)
                if mongo_op:
                    mongo_query[field] = {mongo_op: val}
                else:
                    mongo_query[field] = val
            else:
                mongo_query[key] = val

        return mongo_query

    def close(self):
        # No explicit close needed in pymongo, but can be implemented
        pass
