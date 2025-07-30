from restbase.config import load_config
from restbase.api import fetch_api_data
from restbase.schema import infer_sql_schema
from restbase.db import get_pg_connection, create_table_and_insert

def main():
    config = load_config()
    print("Configuration loaded.")

    api_data = fetch_api_data(config["api"])

    for endpoint, records in api_data.items():
        print(f"\n📜 Preview from {endpoint}:")
        if isinstance(records, list):
            for item in records[:2]:
                print(item)
        else:
            print(records)

    print("\n📆 Inferred SQL table definitions:")
    for endpoint, records in api_data.items():
        if not records:
            print(f"⚠️  No data from {endpoint}, skipping...")
            continue

        table_name = endpoint.strip("/").replace("/", "_")
        try:
            create_sql = infer_sql_schema(records, table_name)
            print(f"\n📄 Table: {table_name}")
            print(create_sql)
        except Exception as e:
            print(f"❌ Failed to infer schema for {endpoint}: {e}")

    print("\n💠 Connecting to PostgreSQL...")
    conn = get_pg_connection(config["postgres"])
    print("✅ Connected to PostgreSQL.")

    for endpoint, records in api_data.items():
        if not records:
            continue
        table_name = endpoint.strip("/").replace("/", "_")
        try:
            create_sql = infer_sql_schema(records, table_name)
            create_table_and_insert(conn, table_name, create_sql, records)
        except Exception as e:
            print(f"❌ Failed to store data for {endpoint}: {e}")

    conn.close()
    print("🌟 Done!")