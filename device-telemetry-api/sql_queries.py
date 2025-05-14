# sql_queries.py

"""
SQL Query Generator Module

This module provides utility functions to dynamically generate SQL queries 
used by the telemetry REST API. It supports both standard INSERT operations 
and INSERT with ON DUPLICATE KEY UPDATE for upserts.
"""

def get_insert_query(table_name, columns):
    """
    Generate a basic SQL INSERT query for the given table and columns.

    This query is used when table_config specifies a simple 'insert' strategy,
    meaning duplicate keys will result in an error (e.g., 409 Conflict).

    Args:
        table_name (str): Name of the target MySQL table.
        columns (list): List of column names for which values will be inserted.

    Returns:
        str: A formatted SQL INSERT query string.
    """
    # Build comma-separated placeholder string for values
    placeholders = ', '.join(['%s'] * len(columns))
    # Format the list of column names
    columns_formatted = ', '.join(columns)
    # Assemble the final query string
    query = f"INSERT INTO {table_name} ({columns_formatted}) VALUES ({placeholders})"
    return query

def get_insert_or_replace_query(table_name, columns):
    """
    Generate an SQL INSERT ... ON DUPLICATE KEY UPDATE query.

    This is used when table_config specifies 'insert_or_replace',
    which allows existing records with duplicate keys to be updated.

    Args:
        table_name (str): Name of the target MySQL table.
        columns (list): List of column names for which values will be inserted.

    Returns:
        str: A formatted SQL UPSERT query that updates on conflict.
    """
    # Build placeholders and column name lists
    placeholders = ', '.join(['%s'] * len(columns))
    columns_formatted = ', '.join(columns)
    # Build update clause to update each column with its new value
    updates = ', '.join([f"{col}=VALUES({col})" for col in columns])
    # Assemble the final query string with ON DUPLICATE KEY UPDATE
    query = f"INSERT INTO {table_name} ({columns_formatted}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {updates}"
    return query
