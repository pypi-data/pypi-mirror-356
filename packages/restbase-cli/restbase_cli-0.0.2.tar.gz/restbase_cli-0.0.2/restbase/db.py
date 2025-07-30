import psycopg2
from psycopg2.extras import Json

def get_pg_connection(pg_config):
    conn = psycopg2.connect(
        host=pg_config['host'],
        port=pg_config['port'],
        dbname=pg_config['dbname'],
        user=pg_config['user'],
        password=pg_config['password']
    )
    conn.autocommit = True
    return conn

def create_table_and_insert(conn, table_name, create_sql, records):
    with conn.cursor() as cur:
        print(f"💠 Creating table '{table_name}'...")
        cur.execute(create_sql)

        if not records:
            print(f"⚠️  No records to insert into {table_name}")
            return

        keys = records[0].keys()
        columns = ', '.join(f'"{k}"' for k in keys)
        values_template = ', '.join(['%s'] * len(keys))
        insert_sql = f'INSERT INTO "{table_name}" ({columns}) VALUES ({values_template})'

        print(f"📅 Inserting {len(records)} records into '{table_name}'...")

        for record in records:
            row = [Json(value) if isinstance(value, (dict, list)) else value for key, value in record.items()]
            cur.execute(insert_sql, row)