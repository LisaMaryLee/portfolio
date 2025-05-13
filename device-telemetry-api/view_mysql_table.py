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

try:
    conn = mysql.connector.connect(
        host=config.Config.MYSQL_HOST,
        user=config.Config.MYSQL_USER,
        password=config.Config.MYSQL_PASSWORD,
        database=config.Config.MYSQL_DB
    )
    cursor = conn.cursor()

    for table in tables:
        columns = table_definitions.columns[table]
        fields = ", ".join(columns)
        order_column = columns[0]

        print(f"\n🔍 Querying table: {table}\n")
        cursor.execute(f"SELECT {fields} FROM {table} ORDER BY {order_column} DESC LIMIT 20")
        rows = cursor.fetchall()

        if rows:
            print(tabulate(rows, headers=columns, tablefmt="grid"))
        else:
            print("⚠️ No data found.")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")
