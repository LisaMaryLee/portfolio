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

# Base URL for API requests, pulled from the same config used by the app
BASE_URL = f"http://{Config.MYSQL_HOST}:5000"

# Dictionary to track results for each table tested
summary = {}

# Helper function to print and store the result of each test
def print_result(table, test_name, expected, actual):
    status = "✅ PASS" if expected == actual else "❌ FAIL"
    print(f"{status} | {test_name:<30} | Expected: {expected}, Got: {actual} [{table}]")
    summary.setdefault(table, []).append((status, test_name, expected, actual))

# Main function to run all negative test cases per model
def run_negative_tests():
    print("🔍 Running negative test coverage...\n")

    # Loop through all registered models (tables)
    for table, model in models.items():
        print(f"🧪 Testing endpoint: /{table}")
        url = f"{BASE_URL}/{table}"

        # ---- 400 Bad Request: Missing key ----
        # Remove the first key from the model to simulate missing required field
        partial_data = {key: "dummy" for key in list(model.keys())[1:]}
        r = requests.post(url, json=partial_data)
        print_result(table, "400 Missing key", 400, r.status_code)

        # ---- 400 Bad Request: Wrong type ----
        # Send Boolean values where strings/integers/floats are expected
        wrong_data = {key: True for key in model.keys()}
        r = requests.post(url, json=wrong_data)
        print_result(table, "400 Wrong type", 400, r.status_code)

        # ---- 400 Bad Request: Malformed JSON ----
        # Simulate invalid JSON payload
        r = requests.post(url, data="{invalid json", headers={"Content-Type": "application/json"})
        print_result(table, "400 Malformed JSON", 400, r.status_code)

        # ---- 401 Unauthorized: Simulated ----
        # Trigger mock 401 via invalid Authorization header
        r = requests.post(url, json={}, headers={"Authorization": "BadToken"})
        print_result(table, "401 Unauthorized (mocked)", 401, r.status_code)

        # ---- 403 Forbidden: Simulated ----
        # Trigger mock 403 via X-Permissions header
        r = requests.post(url, json={}, headers={"X-Permissions": "none"})
        print_result(table, "403 Forbidden (mocked)", 403, r.status_code)

        # ---- 500 Internal Server Error: Simulated ----
        # Inject unexpected field to trigger internal failure
        bad_data = {**{k: "test" for k in model.keys()}, "bad_column": "trigger"}
        r = requests.post(url, json=bad_data)
        print_result(table, "500 Internal error", 500, r.status_code)

    # ---- 404 Not Found: Invalid Endpoint ----
    # Test an endpoint that doesn't exist
    table = "Invalid Endpoint"
    r = requests.post(f"{BASE_URL}/nonexistent_table", json={})
    print_result(table, "404 Not Found", 404, r.status_code)

# Function to print final test summary grouped by table
def print_summary():
    print("\n📊 SUMMARY:")
    for table, results in summary.items():
        print(f"\nTable: {table}")
        for status, test_name, expected, actual in results:
            print(f"  - {status} | {test_name:<30} | Expected {expected}, Got {actual}")

# Entry point for the test script
if __name__ == "__main__":
    run_negative_tests()
    print_summary()
