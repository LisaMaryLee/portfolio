#!/bin/bash
set -e

APP_DIR="$HOME/restapi-samples"
PYTHON_BIN="$APP_DIR/venv/bin/python"
SCRIPT_NAME="dt_RESTAPI.py"
MYSQL_ROOT_PASSWORD="ChangeThisPassword123"
DB_NAME="servostack_REST"
DB_USER="1anonusage"
DB_PASSWORD="eV|76Lf/yoPZ7!3$"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "🛠️ Installing required packages..."
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git curl ufw nginx mysql-server

echo "🔒 Configuring MySQL..."
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}'; FLUSH PRIVILEGES;"
sudo mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME};"
sudo mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';"
sudo mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
sudo mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "FLUSH PRIVILEGES;"

echo "📁 Setting up Python project directory and virtual environment..."
mkdir -p $APP_DIR
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install flask flask-restx mysql-connector-python

echo "📄 Copying project files from script directory: $SCRIPT_DIR"
cp "$SCRIPT_DIR/dt_RESTAPI.py" "$APP_DIR/"
cp "$SCRIPT_DIR/config.py" "$APP_DIR/"
cp "$SCRIPT_DIR/sql_queries.py" "$APP_DIR/"
cp "$SCRIPT_DIR/table_definitions.py" "$APP_DIR/"

echo "⚙️ Creating systemd service..."
sudo bash -c "cat > /etc/systemd/system/servostack_restapi.service" <<EOF
[Unit]
Description=Servostack REST API using Flask
After=network.target mysql.service

[Service]
User=$USER
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$PYTHON_BIN $APP_DIR/$SCRIPT_NAME

[Install]
WantedBy=multi-user.target
EOF

echo "📡 Enabling and starting service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable servostack_restapi.service
sudo systemctl start servostack_restapi.service

echo "🔐 Opening firewall port 5000..."
sudo ufw allow OpenSSH
sudo ufw allow 5000/tcp
sudo ufw --force enable

INTERNAL_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "✅ Setup complete!"
echo "📍 Swagger UI available at: http://${INTERNAL_IP}:5000/"