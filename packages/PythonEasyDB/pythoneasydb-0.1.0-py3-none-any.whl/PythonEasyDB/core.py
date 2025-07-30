import json
from PythonEasyDB.engines.sqlite_engine import SQLiteEngine
from PythonEasyDB.engines.postgres_engine import PostgresEngine
from PythonEasyDB.engines.redis_engine import RedisEngine
from PythonEasyDB.engines.mongo_engine import MongoEngine  # Placeholder for future MongoDB support
from PythonEasyDB.utils import DBError
import re

VALID_TYPES = {"str", "int", "float", "bool", "date", "datetime", "json"}

def is_valid_identifier(name: str) -> bool:
    # SQL identifiers: start with letter or underscore, followed by letters, digits, underscores
    return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name))


class asroDB:
    """
    Unified Database Interface for multiple database engines.
    Supports SQLite, PostgreSQL, MongoDB, and Redis.
    """

    def __init__(self, url: str):
        if url.startswith("sqlite://"):
            path = url.replace("sqlite://", "", 1)
            self.engine = SQLiteEngine(path)
        elif url.startswith("postgresql://"):
            self.engine = PostgresEngine(url)
        elif url.startswith("mongodb://"):
            self.engine = MongoEngine(url)
        elif url.startswith("redis://"):
            self.engine = RedisEngine(url)
        else:
            raise DBError("Unsupported database type.")

    def create_table(self, table_name, **columns):
        """
        Create a new table with the specified name and columns.
        Columns can be defined as:
        - str: column type (e.g., "str", "int", "float")
        - dict: column properties with keys like "type", "primary_key", "auto_increment", "unique", "not_null", "default", "foreign_key"
        - "foreign_key" should be a tuple (ref_table, ref_column) for foreign key references.
        Parameters:
        - table_name (str): Name of the table to create.
        - columns (dict): Column definitions where keys are column names and values are either a string type or a dict of properties.
        Raises:
        - DBError: If the table name is invalid, no columns are defined, or any column definition is invalid.

        """
        if not is_valid_identifier(table_name):
            raise DBError(f"Invalid table name: '{table_name}'. Must be a valid SQL identifier.")
        if not columns:
            raise DBError("At least one column must be defined.")
        for col_name, props in columns.items():
            if not is_valid_identifier(col_name):
                raise DBError(f"Invalid column name: '{col_name}'. Must be a valid SQL identifier.")
            if isinstance(props, str):
                columns[col_name] = {"type": props}
                props = columns[col_name]
            elif not isinstance(props, dict):
                raise DBError(f"Column properties for '{col_name}' must be a string or a dictionary.")
            if "type" not in props:
                raise DBError(f"Column '{col_name}' must have a 'type' defined.")
            if props["type"] not in VALID_TYPES:
                raise DBError(f"Unsupported type '{props['type']}' for column '{col_name}'. Supported types are: {', '.join(VALID_TYPES)}.")
            for bool_field in ["primary_key", "auto_increment", "unique", "not_null"]:
                if bool_field in props and not isinstance(props[bool_field], bool):
                    raise DBError(f"'{bool_field}' for column '{col_name}' must be a boolean.")
            if "default" in props and not isinstance(props["default"], (str, int, float, bool)):
                raise DBError(f"'default' for column '{col_name}' must be a string, int, float, or bool.")
            if "foreign_key" in props:
                fk = props["foreign_key"]
                if not (isinstance(fk, tuple) and len(fk) == 2):
                    raise DBError(f"'foreign_key' for column '{col_name}' must be a tuple (ref_table, ref_column).")
                if not all(is_valid_identifier(x) for x in fk):
                    raise DBError(f"Both elements of 'foreign_key' for column '{col_name}' must be valid SQL identifiers.")
        self.engine.create_table(table_name, **columns)

    def insert(self, table_name, data):
        """
        Insert a new record into the specified table.
        Parameters:
        - table_name (str): Name of the table to insert into.
        - data (dict): Dictionary of column names and values to insert.
        Raises:
        - DBError: If the table name is invalid, data is not a dictionary, or any column name is invalid.
        - If the table does not exist or columns are invalid.
        - If the data contains unsupported types or cannot be serialized.
        """
        if not is_valid_identifier(table_name):
            raise DBError(f"Invalid table name: '{table_name}'. Must be a valid SQL identifier.")
        if not isinstance(data, dict):
            raise DBError("Data to insert must be a dictionary.")
        if not data:
            raise DBError("Data to insert cannot be empty.")
        for col_name in data.keys():
            if not is_valid_identifier(col_name):
                raise DBError(f"Invalid column name: '{col_name}'. Must be a valid SQL identifier.")
        # Check if table exists and columns are valid
        if not self.engine.table_exists(table_name):
            raise DBError(f"Table '{table_name}' does not exist.")
        table_cols = self.engine.get_table_columns(table_name)
        if not all(col in table_cols for col in data.keys()):
            raise DBError(f"Invalid columns for table '{table_name}': {list(data.keys())}")

        # Process data: convert dicts to JSON strings, allow None if column nullable
        for col_name, value in data.items():
            if value is None:
                # Optionally, you can check if column is nullable here
                continue
            if not isinstance(value, (str, int, float, bool, dict)):
                raise DBError(f"Unsupported type for column '{col_name}': {type(value).__name__}. Supported types are: str, int, float, bool, json.")
            if isinstance(value, dict):
                try:
                    data[col_name] = json.dumps(value)
                except TypeError as e:
                    raise DBError(f"Could not serialize value for column '{col_name}': {e}")
        self.engine.insert(table_name, data)

    def select(self, table_name, where=None, order_by=None, desc=False,
               limit=None, offset=None, group_by=None, having=None,
               distinct=False, joins=None):
        """
        Select records from the specified table with optional filtering, sorting, and pagination.
        Parameters:
        - table_name (str): Name of the table to select from.
        - where (dict): Optional dictionary of conditions to filter records.
        - order_by (str): Optional column name to sort by.
        - desc (bool): Whether to sort in descending order (default is False).
        - limit (int): Optional limit on the number of records to return.
        - offset (int): Optional offset for pagination.
        - group_by (str): Optional column name to group by.
        - having (dict): Optional dictionary of conditions to filter grouped records.
        - distinct (bool): Whether to return distinct records (default is False).
        - joins (list): Optional list of tuples for joining other tables, each tuple is (table_name, on_condition).
        Raises:
        - DBError: If the table name is invalid, where clause is not a dictionary,
        - order_by or group_by is not a valid SQL identifier, having clause is not a dictionary,
        - joins is not a list of tuples, or if any join table name is invalid.
        - If the table does not exist or columns in where, order_by, group_by, or having are invalid.
        """
        if not is_valid_identifier(table_name):
            raise DBError(f"Invalid table name: '{table_name}'. Must be a valid SQL identifier.")
        if where is not None and not isinstance(where, dict):
            raise DBError("Where clause must be a dictionary.")
        if order_by is not None and not is_valid_identifier(order_by):
            raise DBError("Order by must be a valid SQL identifier.")
        if group_by is not None and not is_valid_identifier(group_by):
            raise DBError("Group by must be a valid SQL identifier.")
        if having is not None and not isinstance(having, dict):
            raise DBError("Having clause must be a dictionary.")
        if joins is not None:
            if not isinstance(joins, list):
                raise DBError("Joins must be a list of tuples (table_name, on_condition).")
            for join in joins:
                if not (isinstance(join, tuple) and len(join) == 2):
                    raise DBError("Each join must be a tuple (table_name, on_condition).")
                if not is_valid_identifier(join[0]):
                    raise DBError(f"Invalid join table name: '{join[0]}'. Must be valid SQL identifier.")
                # on_condition is a SQL string; skipping strict validation

        if not self.engine.table_exists(table_name):
            raise DBError(f"Table '{table_name}' does not exist.")
        table_cols = self.engine.get_table_columns(table_name)

        if where and not all(col in table_cols for col in where.keys()):
            raise DBError(f"Invalid columns in where clause for table '{table_name}': {list(where.keys())}")
        if order_by and order_by not in table_cols:
            raise DBError(f"Invalid order by column '{order_by}' for table '{table_name}'.")
        if group_by and group_by not in table_cols:
            raise DBError(f"Invalid group by column '{group_by}' for table '{table_name}'.")
        if having and group_by is None:
            raise DBError("Having clause can only be used with a group by clause.")
        if having and not all(col in table_cols for col in having.keys()):
            raise DBError(f"Invalid columns in having clause for table '{table_name}': {list(having.keys())}")
        if distinct and order_by:
            raise DBError("Distinct cannot be used with order by. Please remove one of them.")
        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                raise DBError("Limit must be a non-negative integer.")
        if offset is not None:
            if not isinstance(offset, int) or offset < 0:
                raise DBError("Offset must be a non-negative integer.")

        # Check join tables and columns if possible
        if joins is not None:
            for join_table, on_condition in joins:
                if not self.engine.table_exists(join_table):
                    raise DBError(f"Join table '{join_table}' does not exist.")
                # Skipping detailed on_condition columns check for now

        return self.engine.select(table_name, where, order_by, desc,
                                  limit, offset, group_by, having,
                                  distinct, joins)

    def update(self, table_name, where, values):
        """
        Update records in the specified table based on the where clause.
        Parameters:
        - table_name (str): Name of the table to update.
        - where (dict): Dictionary of conditions to filter which records to update.
        - values (dict): Dictionary of column names and new values to set.
        Raises:
        - DBError: If the table name is invalid, where clause or values are not dictionaries,
        - if any column name is invalid, or if the table does not exist.
        - If the where clause or values contain unsupported types or cannot be serialized.
        """
        if not is_valid_identifier(table_name):
            raise DBError(f"Invalid table name: '{table_name}'. Must be a valid SQL identifier.")
        if not isinstance(where, dict) or not where:
            raise DBError("Where clause must be a non-empty dictionary.")
        if not isinstance(values, dict) or not values:
            raise DBError("Values to update must be a non-empty dictionary.")
        for col_name in values.keys():
            if not is_valid_identifier(col_name):
                raise DBError(f"Invalid column name: '{col_name}'. Must be a valid SQL identifier.")

        if not self.engine.table_exists(table_name):
            raise DBError(f"Table '{table_name}' does not exist.")
        table_cols = self.engine.get_table_columns(table_name)
        if not all(col in table_cols for col in where.keys()):
            raise DBError(f"Invalid columns in where clause for table '{table_name}': {list(where.keys())}")
        if not all(col in table_cols for col in values.keys()):
            raise DBError(f"Invalid columns in values for table '{table_name}': {list(values.keys())}")

        # Serialize dict values to JSON in update values
        for k, v in values.items():
            if isinstance(v, dict):
                try:
                    values[k] = json.dumps(v)
                except TypeError as e:
                    raise DBError(f"Could not serialize value for column '{k}': {e}")

        self.engine.update(table_name, where, values)

    def delete(self, table_name, where):
        """
        Delete records from the specified table based on the where clause.
        Parameters:
        - table_name (str): Name of the table to delete from.
        - where (dict): Dictionary of conditions to filter which records to delete.
        Raises:
        - DBError: If the table name is invalid, where clause is not a dictionary,
        - if any column name is invalid, or if the table does not exist.
        - If the where clause contains unsupported types or cannot be serialized.
        """
        if not is_valid_identifier(table_name):
            raise DBError(f"Invalid table name: '{table_name}'. Must be a valid SQL identifier.")
        if not isinstance(where, dict) or not where:
            raise DBError("Where clause must be a non-empty dictionary.")
        for col_name in where.keys():
            if not is_valid_identifier(col_name):
                raise DBError(f"Invalid column name: '{col_name}'. Must be a valid SQL identifier.")

        if not self.engine.table_exists(table_name):
            raise DBError(f"Table '{table_name}' does not exist.")
        table_cols = self.engine.get_table_columns(table_name)
        if not all(col in table_cols for col in where.keys()):
            raise DBError(f"Invalid columns in where clause for table '{table_name}': {list(where.keys())}")

        self.engine.delete(table_name, where)

    def close(self):
        if hasattr(self.engine, 'close'):
            self.engine.close()
