# 📡 Device Telemetry API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
[![Flask REST API](https://img.shields.io/badge/Framework-Flask-blue.svg)](https://flask.palletsprojects.com/) 
[![Python](https://img.shields.io/badge/Python-3.7%2B-green.svg)](https://www.python.org/downloads/)

A lightweight Flask REST API for collecting and viewing anonymized device telemetry from storage appliances. Supports real-time ingestion, dynamic Swagger documentation, and easy table viewing via a web-based UI.

---

## 🚀 Features

- ✅ Swagger/OpenAPI documentation for all endpoints
- ✅ Runtime validation of input types with error simulation for testing
- ✅ Dynamic endpoint generation from `table_definitions.py`
- ✅ Integrated viewer to browse last 20 entries from each table
- ✅ Includes negative test automation (`test_negative.py`)
- ✅ Support for `INSERT` and `INSERT OR REPLACE` per-table config

---

## 📁 Project Structure

```
device-telemetry-api/
├── config.py                     # MySQL connection settings
├── dt_RESTAPI.py                # Main Flask API
├── sql_queries.py               # SQL insert/upsert generators
├── table_definitions.py         # Table schemas + Swagger models
├── viewer_route.py              # Viewer UI for table data
├── test_negative.py             # Negative scenario test script
├── test_dynamic_api_load.py     # Load test with random values
├── requirements.txt             # Dependencies
├── stack_restapi.service        # Systemd service template
├── setup/                       # Install & uninstall bash scripts
└── README.md                    # You are here
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/LisaMaryLee/samples.git
cd samples/device-telemetry-api
```

### 2. Configure MySQL Credentials
Update `config.py` with your actual DB credentials:
```python
class Config:
    MYSQL_HOST = "localhost"
    MYSQL_USER = "your_user"
    MYSQL_PASSWORD = "your_password"
    MYSQL_DB = "your_database"
```

### 3. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Start the API
```bash
python3 dt_RESTAPI.py
```

The API will be available at: `http://localhost:5000/`

---

## 🧪 Testing the API

### Negative Scenario Tests
Run:
```bash
python3 test_negative.py
```

### Random Load Tests
```bash
python3 test_dynamic_api_load.py 10
```
This sends 10 random payloads to each endpoint.

---

## 👀 View Telemetry Data in Browser

Go to:
```
http://localhost:5000/viewer
```
Use the dropdown to select a table and view its most recent entries.

---

## 🔥 Systemd Integration (Optional)

You can register the API as a service:

### `stack_restapi.service`
```ini
[Unit]
Description=Device Telemetry REST API
After=network.target mysql.service

[Service]
User=%i
WorkingDirectory=%h/samples/device-telemetry-api
ExecStart=%h/samples/device-telemetry-api/venv/bin/python3 %h/samples/device-telemetry-api/dt_RESTAPI.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then run:
```bash
sudo cp stack_restapi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable stack_restapi
sudo systemctl start stack_restapi
```

To uninstall:
```bash
bash ./setup/uninstall_restapi.sh
```

---

## 📎 Dependencies

### `requirements.txt`
```text
flask
flask-restx
mysql-connector-python
tabulate
faker
```
Install them with:
```bash
pip install -r requirements.txt
```

---

## 📌 Notes

- The API supports both `insert` and `insert_or_replace` logic per table.
- Schema definitions and field-level types are stored in `table_definitions.py`.
- Swagger UI is served by default at the root (`/`) of the app.

---

## 🧑‍💻 Author

**Lisa Mary Lee**  
💼 [LinkedIn](https://www.linkedin.com/in/lisamarylee)  
📫 lisamarylee@gmail.com

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

### LICENSE
```text
MIT License

Copyright (c) 2025 Lisa Mary Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
