# sql_queries.py

def get_insert_query(table_name, columns):
    """
    Generates an SQL INSERT query for a given table and columns.

    Parameters:
        table_name (str): The name of the table to insert into.
        columns (list): A list of column names to insert values into.

    Returns:
        str: The formatted SQL INSERT query string.
    """
    placeholders = ', '.join(['%s'] * len(columns))
    columns_formatted = ', '.join(columns)
    query = f"INSERT INTO {table_name} ({columns_formatted}) VALUES ({placeholders})"
    return query

def get_insert_or_replace_query(table_name, columns):
    """
    Generates an SQL INSERT query with ON DUPLICATE KEY UPDATE for a given table and columns.
    This query will insert new records or update existing records if a duplicate key is found.

    Parameters:
        table_name (str): The name of the table to insert into.
        columns (list): A list of column names to insert values into.

    Returns:
        str: The formatted SQL INSERT ON DUPLICATE KEY UPDATE query string.
    """
    placeholders = ', '.join(['%s'] * len(columns))
    columns_formatted = ', '.join(columns)
    updates = ', '.join([f"{col}=VALUES({col})" for col in columns])
    query = f"INSERT INTO {table_name} ({columns_formatted}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {updates}"
    return query

