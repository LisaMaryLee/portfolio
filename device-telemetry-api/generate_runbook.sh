#!/bin/bash

RUNBOOK="runbook_device_telemetry.md"

cat > $RUNBOOK <<EOF
# 📘 Device Telemetry Intake API – Ubuntu Server Runbook

## ✅ System Requirements
- Ubuntu 20.04+ (Debian-based)
- Python 3.8+
- MySQL Server 8+
- pip + venv
- Port 5000 open (or reverse proxied)

---

## 🔧 Step 1: Install System Dependencies
\`\`\`bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv mysql-server
\`\`\`

---

## 🗃️ Step 2: Setup MySQL
\`\`\`bash
sudo systemctl start mysql
sudo mysql_secure_installation

# Login and run schema creation
mysql -u root -p < create_device_telemetry_schema.sql
\`\`\`

---

## 🐍 Step 3: Create Python Virtual Environment
\`\`\`bash
cd ~/device-telemetry-intake-api
python3 -m venv venv
source venv/bin/activate
pip install flask flask-restx mysql-connector-python
\`\`\`

---

## ⚙️ Step 4: Set Up Config
\`\`\`python
# config.py
class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'youruser'
    MYSQL_PASSWORD = 'yourpass'
    MYSQL_DB = 'servostack_REST'
\`\`\`

---

## 🚀 Step 5: Run the API
\`\`\`bash
python servostack_RESTAPI.py
\`\`\`

Access at: `http://your-server-ip:5000/`

---

## 🔁 Optional: Systemd Service
Create `/etc/systemd/system/device-telemetry.service`:
\`\`\`ini
[Unit]
Description=Device Telemetry Intake API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/device-telemetry-intake-api
ExecStart=/home/ubuntu/device-telemetry-intake-api/venv/bin/python servostack_RESTAPI.py
Restart=always

[Install]
WantedBy=multi-user.target
\`\`\`

\`\`\`bash
sudo systemctl daemon-reexec
sudo systemctl enable device-telemetry.service
sudo systemctl start device-telemetry.service
\`\`\`

---

## 🧪 Test Example Endpoint
\`\`\`bash
curl -X POST http://localhost:5000/ss_general -H "Content-Type: application/json" -d '{
  "SID": "999123456789",
  "ss_software_version": "X.2.6",
  "model_number": "qs4v2",
  "time_zone": "UTC",
  "locale": "en_US",
  "dock_firmware_version": "18",
  "dock_qty": 4
}'
\`\`\`

---

## 📄 Logs & Debugging
- API log (if using systemd): \`journalctl -u device-telemetry.service\`
- MySQL errors: \`/var/log/mysql/error.log\`

EOF

echo "✅ Runbook created: $RUNBOOK"
