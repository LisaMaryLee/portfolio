# Stack REST API

This project provides a dynamic, table-aware REST API for ingesting anonymized device telemetry data into a MySQL database using Flask and Flask-RESTX.

## 📦 Features

- REST API endpoints dynamically generated for each telemetry table
- Swagger UI auto-generated for documentation and testing
- MySQL schema versioned in `create_device_telemetry_schema.sql`
- Systemd service integration for persistent API hosting
- Test data loader and terminal-based MySQL viewer included

## 🚀 Setup Instructions

1. Clone the repo and run the setup script:

```bash
chmod +x setup_from_repo_restapi_ssh.sh
./setup_from_repo_restapi_ssh.sh
```

2. Optional: Create a `.env` file inside `~/restapi-telemetry` to override MySQL credentials.

```env
MYSQL_HOST=localhost
MYSQL_USER=anonusage
MYSQL_PASSWORD=your-password
MYSQL_DB=stack_REST
```

## ✅ Running Services

- REST API: [http://<your-ip>:5000/](http://<your-ip>:5000/)
- Live view MySQL Tables: [http://<your-ip>:5000/viewer](http://<your-ip>:5000/)
- Terminal MySQL viewer: `python3 view_mysql_table.py`
- Dynamic test loader: `python3 test_dynamic_api_load.py 10`

---

## ➕ Adding New Tables

1. **Update Schema**

Edit `create_device_telemetry_schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS ss_network_config (
  SID VARCHAR(32) NOT NULL,
  interface_name VARCHAR(64),
  ip_address VARCHAR(64),
  mac_address VARCHAR(64),
  PRIMARY KEY (SID, interface_name)
);
```

2. **Update `table_definitions.py`**

```python
columns['ss_network_config'] = [
    'SID', 'interface_name', 'ip_address', 'mac_address'
]

ss_network_config_model = {
    'SID': fields.String(required=True),
    'interface_name': fields.String(required=True),
    'ip_address': fields.String(required=True),
    'mac_address': fields.String(required=True)
}

table_config['ss_network_config'] = 'insert_or_replace'
models['ss_network_config'] = ss_network_config_model
```

3. **Restart Service**

```bash
sudo systemctl restart servostack_restapi.service
```

New endpoint: `POST /ss_network_config`

---

## ✏️ Adding Columns to Existing Tables

1. Modify the SQL schema with `ALTER TABLE`.

2. Update `columns[...]` and the matching Swagger model in `table_definitions.py`.

3. Restart the service.

---

## 🔧 Uninstall Script

To remove the service, files, and MySQL database:

```bash
chmod +x uninstall_restapi_env.sh
./uninstall_restapi_env.sh
```

---

## 🧪 Testing & Observability

- Use `test_dynamic_api_load.py` to inject test data
- Use `view_mysql_table.py` to view tables from the terminal
