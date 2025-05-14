#!/usr/bin/env python3
# test_dynamic_api_load.py
#
# Purpose:
#   This script sends random data to all REST API endpoints defined in table_definitions.py.
#   It dynamically loads the table structure, generates fake data for each model, and POSTs
#   to the associated endpoint for load and integration testing.

import requests
import random
import sys
import importlib.util
from datetime import datetime
from faker import Faker

# Dynamically load table_definitions.py as a module (avoids import cycles or static linking)
spec = importlib.util.spec_from_file_location("table_definitions", "./table_definitions.py")
table_definitions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(table_definitions)

# Base URL of the local running API
BASE_URL = "http://localhost:5000"

# Faker instance for generating dummy values
faker = Faker()

# Read number of test requests per endpoint from command-line argument, default is 10
run_count = int(sys.argv[1]) if len(sys.argv) > 1 else 10

# Function: generate random data based on field type
def random_value(field_type):
    if field_type == 'String':
        return faker.word()
    if field_type == 'Integer':
        return random.randint(1, 100)
    if field_type == 'Float':
        return round(random.uniform(1.0, 100.0), 2)
    return "sample"

# Function: extract expected model structure and fill it with randomized data
def extract_fields(model):
    return {key: random_value(type(value).__name__) for key, value in model.items()}

# Begin testing loop for each registered endpoint
print(f"📡 Sending {run_count} requests to each API endpoint...")

for name, model in table_definitions.models.items():
    url = f"{BASE_URL}/{name}"
    for i in range(run_count):
        # Generate a payload based on model structure
        payload = extract_fields(model)

        # Special handling for SID field to ensure realistic ID format
        if 'SID' in payload:
            payload['SID'] = str(random.randint(10**15, 10**16 - 1))

        # Add ISO timestamp if required by the model
        if 'timestamp' in payload:
            payload['timestamp'] = datetime.now().isoformat()

        # Attempt to POST the payload to the corresponding endpoint
        try:
            response = requests.post(url, json=payload)
            print(f"{name} [{i+1}]: {response.status_code}")
        except Exception as e:
            print(f"❌ Error posting to {url}: {e}")
