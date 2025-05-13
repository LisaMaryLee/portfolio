#!/usr/bin/env python3

"""
Extended test script for validating REST API error handling on all endpoints.
Covers:
- 400: Invalid JSON or missing fields
- 401: Unauthorized (mocked)
- 403: Forbidden (mocked)
- 404: Not Found (invalid endpoint)
- 500: Internal Server Error (simulate bad query)
"""

import requests
import json
from table_definitions import models
from config import Config

BASE_URL = f"http://{Config.MYSQL_HOST}:5000"

def run_negative_tests():
    for table, model in models.items():
        print(f"🧪 Testing endpoint: /{table}")
        url = f"{BASE_URL}/{table}"

        # 400: Missing required field
        partial_data = {key: "dummy" for key in list(model.keys())[1:]}
        r = requests.post(url, json=partial_data)
        print(f"400 Missing key: {r.status_code} {r.reason}")

        # 400: Wrong data types
        wrong_data = {key: 12345 for key in model.keys()}
        r = requests.post(url, json=wrong_data)
        print(f"400 Wrong type: {r.status_code} {r.reason}")

        # 400: Invalid JSON
        r = requests.post(url, data="not json", headers={"Content-Type": "application/json"})
        print(f"400 Malformed JSON: {r.status_code} {r.reason}")

        # 401: Unauthorized (simulate with header, though not enforced)
        r = requests.post(url, json={}, headers={"Authorization": "InvalidToken"})
        print(f"401 Unauthorized (mocked): {r.status_code} {r.reason}")

        # 403: Forbidden (simulate with invalid permissions header)
        r = requests.post(url, json={}, headers={"X-Permissions": "none"})
        print(f"403 Forbidden (mocked): {r.status_code} {r.reason}")

        print("-" * 60)

    # 404: Invalid endpoint
    r = requests.post(f"{BASE_URL}/nonexistent_table", json={})
    print(f"404 Not Found: {r.status_code} {r.reason}")

    # 500: Internal error simulation — bad SQL or missing DB fields
    for table, model in models.items():
        url = f"{BASE_URL}/{table}"
        # Inject unexpected key to trigger DB mismatch
        bad_data = {**{key: "value" for key in model.keys()}, "bad_column": "crash"}
        r = requests.post(url, json=bad_data)
        print(f"500 Internal (bad column): {r.status_code} {r.reason}")
        print("-" * 60)

if __name__ == "__main__":
    run_negative_tests()
