# unidb/utils.py

class DBError(Exception):
    pass

def parse_where(where: dict, placeholder="?"):
    ops = {
        "lt": "<",
        "lte": "<=",
        "gt": ">",
        "gte": ">=",
        "ne": "!=",
        "eq": "=",
        "in": "IN",
        "notin": "NOT IN",
        "like": "LIKE",
        "notlike": "NOT LIKE",
        "isnull": "IS NULL",
        "between": "BETWEEN"
    }

    conditions = []
    values = []

    for key, value in where.items():
        if "__" in key:
            field, op = key.split("__", 1)
            sql_op = ops.get(op, "=")

            if op in ["in", "notin"]:
                placeholders = ", ".join([placeholder] * len(value))
                conditions.append(f"{field} {sql_op} ({placeholders})")
                values.extend(value)

            elif op == "between" and isinstance(value, (list, tuple)) and len(value) == 2:
                conditions.append(f"{field} BETWEEN {placeholder} AND {placeholder}")
                values.extend(value)

            elif op == "isnull":
                if value:
                    conditions.append(f"{field} IS NULL")
                else:
                    conditions.append(f"{field} IS NOT NULL")

            else:
                conditions.append(f"{field} {sql_op} {placeholder}")
                values.append(value)
        else:
            conditions.append(f"{key} = {placeholder}")
            values.append(value)

    clause = " AND ".join(conditions)
    return clause, tuple(values)

def build_select_query(table, where=None, order_by=None, desc=False, limit=None, offset=None, group_by=None, having=None, distinct=False, joins=None, placeholder="?"):
    sql = "SELECT "
    sql += "DISTINCT " if distinct else ""
    sql += f"* FROM {table}"
    values = ()

    if joins:
        for join in joins:
            join_type = join.get("type", "INNER").upper()
            join_table = join["table"]
            join_on = join["on"]
            sql += f" {join_type} JOIN {join_table} ON {join_on}"

    if where:
        where_clause, where_vals = parse_where(where, placeholder)
        sql += f" WHERE {where_clause}"
        values += where_vals

    if group_by:
        sql += f" GROUP BY {group_by}"

    if having:
        having_clause, having_vals = parse_where(having, placeholder)
        sql += f" HAVING {having_clause}"
        values += having_vals

    if order_by:
        sql += f" ORDER BY {order_by}"
        if desc:
            sql += " DESC"

    if limit is not None:
        sql += f" LIMIT {limit}"
        if offset is not None:
            sql += f" OFFSET {offset}"

    return sql, values
