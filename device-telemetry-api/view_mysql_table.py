#!/usr/bin/env python3

# Imports
import mysql.connector                      # For connecting to MySQL
import importlib.util                       # For dynamically loading Python modules
import os                                   # For working with filesystem paths
from tabulate import tabulate               # For printing formatted tables in the console

# --- Dynamically load config.py for DB connection credentials ---
spec_cfg = importlib.util.spec_from_file_location(
    "config",
    os.path.expanduser("~/restapi-telemetry/config.py")
)
config = importlib.util.module_from_spec(spec_cfg)
spec_cfg.loader.exec_module(config)

# --- Dynamically load table_definitions.py for table structure ---
spec_defs = importlib.util.spec_from_file_location(
    "table_definitions",
    os.path.expanduser("~/restapi-telemetry/table_definitions.py")
)
table_definitions = importlib.util.module_from_spec(spec_defs)
spec_defs.loader.exec_module(table_definitions)

# Get a list of telemetry table names
tables = list(table_definitions.models.keys())

try:
    # --- Establish MySQL connection using loaded config values ---
    conn = mysql.connector.connect(
        host=config.Config.MYSQL_HOST,
        user=config.Config.MYSQL_USER,
        password=config.Config.MYSQL_PASSWORD,
        database=config.Config.MYSQL_DB
    )
    cursor = conn.cursor()

    # --- Loop through each telemetry table and query recent records ---
    for table in tables:
        columns = table_definitions.columns[table]   # List of columns for the table
        fields = ", ".join(columns)                  # Format columns for SQL SELECT
        order_column = columns[0]                    # Use first column (usually ID) to sort descending

        print(f"\n🔍 Querying table: {table}\n")
        # Execute query to fetch most recent 20 rows
        cursor.execute(f"SELECT {fields} FROM {table} ORDER BY {order_column} DESC LIMIT 20")
        rows = cursor.fetchall()

        # Pretty-print results in tabular format, or indicate if empty
        if rows:
            print(tabulate(rows, headers=columns, tablefmt="grid"))
        else:
            print("⚠️ No data found.")

    # --- Clean up ---
    cursor.close()
    conn.close()

except Exception as e:
    # Handle and display any connection or query errors
    print(f"❌ Error: {e}")
