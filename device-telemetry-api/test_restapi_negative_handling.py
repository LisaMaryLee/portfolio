#!/usr/bin/env python3

"""
Test script for validating REST API negative scenarios.

Covers:
- 400: Missing required fields, wrong types, malformed JSON
- 401: Unauthorized (simulated)
- 403: Forbidden (simulated)
- 404: Not Found (invalid endpoint)
- 500: Internal Server Error (simulated bad input)
"""

import requests
import json
from table_definitions import models
from config import Config

BASE_URL = f"http://{Config.MYSQL_HOST}:5000"
summary = {}

def print_result(table, test_name, expected, actual):
    key = f"{table}:{test_name}"
    if expected == actual:
        status = "✅ PASS"
    else:
        status = "❌ FAIL"
    print(f"{status} | {test_name:<30} | Expected: {expected} | Got: {actual} [{table}]")
    summary.setdefault(table, []).append((status, test_name, expected, actual))

def run_negative_tests():
    print("🔍 Running negative test coverage...\n")
    for table, model in models.items():
        print(f"🧪 Testing endpoint: /{table}")
        url = f"{BASE_URL}/{table}"

        # 400: Missing key
        partial_data = {key: "dummy" for key in list(model.keys())[1:]}
        r = requests.post(url, json=partial_data)
        print_result(table, "400 Missing key", 400, r.status_code)

        # 400: Wrong type
        wrong_data = {key: 123456 for key in model.keys()}
        r = requests.post(url, json=wrong_data)
        print_result(table, "400 Wrong type", 400, r.status_code)

        # 400: Malformed JSON
        r = requests.post(url, data="not-json", headers={"Content-Type": "application/json"})
        print_result(table, "400 Malformed JSON", 400, r.status_code)

        # 401: Unauthorized (mocked)
        r = requests.post(url, json={}, headers={"Authorization": "BadToken"})
        print_result(table, "401 Unauthorized (mocked)", 401, r.status_code)

        # 403: Forbidden (mocked)
        r = requests.post(url, json={}, headers={"X-Permissions": "none"})
        print_result(table, "403 Forbidden (mocked)", 403, r.status_code)

        # 500: Internal (simulate by inserting invalid column)
        bad_data = {**{k: "fake" for k in model.keys()}, "bad_column": "oops"}
        r = requests.post(url, json=bad_data)
        print_result(table, "500 Internal error", 500, r.status_code)

        print("-" * 70)

    # 404: Not Found
    table = "Invalid Endpoint"
    r = requests.post(f"{BASE_URL}/nonexistent_table", json={})
    print_result(table, "404 Not Found", 404, r.status_code)

def print_summary():
    print("\n📊 SUMMARY:")
    for table, results in summary.items():
        print(f"\nTable: {table}")
        for status, test_name, expected, actual in results:
            print(f"  - {status} | {test_name:<30} | Expected {expected}, Got {actual}")

if __name__ == "__main__":
    run_negative_tests()
    print_summary()
