# config.py
# Secure, environment-aware database configuration for the REST API

import os

class Config:
    # Host where the MySQL server is running (default: 'localhost')
    MYSQL_HOST = os.getenv("MYSQL_HOST")

    # MySQL user with access to the application database
    MYSQL_USER = os.getenv("MYSQL_USER")

    # Password for the above MySQL user
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

    # Name of the database used by the Flask REST API
    MYSQL_DB = os.getenv("MYSQL_DB")
