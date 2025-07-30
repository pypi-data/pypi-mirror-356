def infer_sql_schema(data, table_name):
    if not isinstance(data, list) or not data:
        raise ValueError(f"Cannot infer schema from empty or invalid data for table {table_name}")

    sample = data[0]
    column_defs = []

    for key, value in sample.items():
        sql_type = "TEXT"
        if isinstance(value, bool):
            sql_type = "BOOLEAN"
        elif isinstance(value, int):
            sql_type = "INTEGER"
        elif isinstance(value, float):
            sql_type = "FLOAT"
        elif isinstance(value, (dict, list)):
            sql_type = "JSONB"
        elif isinstance(value, str):
            sql_type = "TEXT"
        elif value is None:
            sql_type = "TEXT"

        column_defs.append(f'"{key}" {sql_type}')

    columns_sql = ",\n  ".join(column_defs)
    return f'CREATE TABLE IF NOT EXISTS "{table_name}" (\n  {columns_sql}\n);'