#!/usr/bin/env python3

import mysql.connector
import importlib.util
import os
from tabulate import tabulate

# Load config.py
spec_cfg = importlib.util.spec_from_file_location("config", os.path.expanduser("~/restapi-telemetry/config.py"))
config = importlib.util.module_from_spec(spec_cfg)
spec_cfg.loader.exec_module(config)

# Load table_definitions.py
spec_defs = importlib.util.spec_from_file_location("table_definitions", os.path.expanduser("~/restapi-telemetry/table_definitions.py"))
table_definitions = importlib.util.module_from_spec(spec_defs)
spec_defs.loader.exec_module(table_definitions)

tables = list(table_definitions.models.keys())
print("\n📋 Available tables:")
for idx, name in enumerate(tables):
    print(f"{idx+1}. {name}")

choice = input("\nEnter the number of the table to view: ").strip()
if not choice.isdigit() or int(choice) < 1 or int(choice) > len(tables):
    print("❌ Invalid choice.")
    exit(1)

table = tables[int(choice) - 1]
columns = table_definitions.columns[table]
fields = ", ".join(columns)
order_column = columns[0]  # Assume first column is primary key or timestamp

print(f"\n🔍 Querying table: {table}\n")

try:
    conn = mysql.connector.connect(
        host=config.Config.MYSQL_HOST,
        user=config.Config.MYSQL_USER,
        password=config.Config.MYSQL_PASSWORD,
        database=config.Config.MYSQL_DB
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT {fields} FROM {table} ORDER BY {order_column} DESC LIMIT 20")
    rows = cursor.fetchall()
    print(tabulate(rows, headers=columns, tablefmt="grid"))

    # Generate HTML
    html_table = tabulate(rows, headers=columns, tablefmt="html")
    html_path = os.path.expanduser(f"~/restapi-telemetry/output_{table}.html")
    with open(html_path, "w") as f:
        f.write(f"<html><head><title>{table} Data</title></head><body><h2>Latest 20 rows from table: {table}</h2>{html_table}</body></html>")

    print(f"\n🌐 HTML output saved to: {html_path}")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()