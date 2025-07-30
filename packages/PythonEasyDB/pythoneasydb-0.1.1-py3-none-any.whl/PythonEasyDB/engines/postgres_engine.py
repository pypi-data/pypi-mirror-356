# unidb/engines/postgres_engine.py

import psycopg2
from psycopg2.extras import RealDictCursor
from PythonEasyDB.utils import DBError, build_select_query

class PostgresEngine:
    def __init__(self, dsn):
        try:
            self.conn = psycopg2.connect(dsn)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            raise DBError(f"Could not connect to PostgreSQL: {e}")

    def create_table(self, table_name, **columns):
        try:
            column_defs = []
            foreign_keys = []

            for col_name, props in columns.items():
                if isinstance(props, str):
                    col_type = self.map_type(props)
                    column_defs.append(f"{col_name} {col_type}")
                    continue

                col_type = self.map_type(props.get("type", "str"))
                definition = [col_name, col_type]

                if props.get("primary_key"):
                    definition.append("PRIMARY KEY")

                if props.get("auto_increment") and col_type.upper() == "SERIAL":
                    pass  # SERIAL already auto-increments

                if props.get("unique"):
                    definition.append("UNIQUE")

                if props.get("not_null"):
                    definition.append("NOT NULL")

                if "default" in props:
                    default_val = props["default"]
                    if isinstance(default_val, str):
                        default_val = f"'{default_val}'"
                    definition.append(f"DEFAULT {default_val}")

                if "foreign_key" in props:
                    ref_table, ref_column = props["foreign_key"]
                    fk = f"FOREIGN KEY ({col_name}) REFERENCES {ref_table}({ref_column})"
                    if props.get("on_delete"):
                        fk += f" ON DELETE {props['on_delete'].upper()}"
                    foreign_keys.append(fk)

                column_defs.append(" ".join(definition))

            all_defs = column_defs + foreign_keys
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(all_defs)})"
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            raise DBError(f"Failed to create table '{table_name}': {e}")

    def insert(self, table_name, data):
        try:
            keys = ", ".join(data.keys())
            placeholders = ", ".join("%s" for _ in data)
            values = tuple(data.values())
            sql = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})"
            self.cursor.execute(sql, values)
            self.conn.commit()
        except Exception as e:
            raise DBError(f"Failed to insert into '{table_name}': {e}")

    def select(self, table_name, where=None, order_by=None, desc=False, limit=None, offset=None, group_by=None, having=None, distinct=False, joins=None):
        try:
            sql, values = build_select_query(
                table=table_name,
                where=where,
                order_by=order_by,
                desc=desc,
                limit=limit,
                offset=offset,
                group_by=group_by,
                having=having,
                distinct=distinct,
                placeholder="%s"
            )
            self.cursor.execute(sql, values)
            return self.cursor.fetchall()
        except Exception as e:
            raise DBError(f"Failed to select from '{table_name}': {e}")

    def update(self, table_name, where, values):
        try:
            set_clause = ", ".join(f"{k}=%s" for k in values)
            set_values = tuple(values.values())

            from unidb.utils import parse_where
            where_clause, where_values = parse_where(where, placeholder="%s")
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

            self.cursor.execute(sql, set_values + where_values)
            self.conn.commit()
        except Exception as e:
            raise DBError(f"Failed to update '{table_name}': {e}")

    def delete(self, table_name, where):
        try:
            from unidb.utils import parse_where
            where_clause, where_values = parse_where(where, placeholder="%s")
            sql = f"DELETE FROM {table_name} WHERE {where_clause}"
            self.cursor.execute(sql, where_values)
            self.conn.commit()
        except Exception as e:
            raise DBError(f"Failed to delete from '{table_name}': {e}")

    def map_type(self, t: str, auto_increment=False):
        t = t.lower()
        if auto_increment and t == "int":
            return "SERIAL"
        return {
            "str": "VARCHAR",
            "int": "INTEGER",
            "float": "REAL",
            "bool": "BOOLEAN"
        }.get(t, "VARCHAR")

    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            raise DBError(f"Failed to close PostgreSQL connection: {e}")
