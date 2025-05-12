#!/usr/bin/env python3
# test_dynamic_api_load.py
# This script sends random data to the API endpoints defined in table_definitions.py.
# It uses the Faker library to generate random values for each field type.  
import requests
import random
import sys
import importlib.util
from datetime import datetime
from faker import Faker

# Load table definitions dynamically
spec = importlib.util.spec_from_file_location("table_definitions", "./table_definitions.py")
table_definitions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(table_definitions)

BASE_URL = "http://localhost:5000"
faker = Faker()
run_count = int(sys.argv[1]) if len(sys.argv) > 1 else 10

# Mapping Flask field types to random generators
def random_value(field_type):
    if field_type == 'String':
        return faker.word()
    if field_type == 'Integer':
        return random.randint(1, 100)
    if field_type == 'Float':
        return round(random.uniform(1.0, 100.0), 2)
    return "sample"

def extract_fields(model):
    return {key: random_value(type(value).__name__) for key, value in model.items()}

print(f"📡 Sending {run_count} requests to each API endpoint...")
for name, model in table_definitions.models.items():
    url = f"{BASE_URL}/{name}"
    for i in range(run_count):
        payload = extract_fields(model)
        if 'SID' in payload:
            payload['SID'] = str(random.randint(10**15, 10**16 - 1))
        if 'timestamp' in payload:
            payload['timestamp'] = datetime.now().isoformat()
        try:
            response = requests.post(url, json=payload)
            print(f"{name} [{i+1}]: {response.status_code}")
        except Exception as e:
            print(f"❌ Error posting to {url}: {e}")
