#!/bin/bash
set -e

REPO_SSH_URL="git@github.com:LisaMaryLee/samples.git"
APP_DIR="$HOME/restapi-samples"
CLONE_DIR="$HOME/samples"
SOURCE_SUBDIR="device-telemetry-api"
PYTHON_BIN="$APP_DIR/venv/bin/python"
SCRIPT_NAME="dt_RESTAPI.py"
MYSQL_ROOT_PASSWORD="ChangeThisPassword123"
DB_NAME="stack_REST"
DB_USER="1anonusage"
DB_PASSWORD="eV|76Lf/yoPZ7!3$"

echo "🛠️ Installing required packages..."
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git curl ufw nginx mysql-server

echo "🔐 Cloning repo using SSH..."
rm -rf $CLONE_DIR
git clone $REPO_SSH_URL $CLONE_DIR

echo "🔓 Launching MySQL as root to configure root login..."
sudo mysql <<EOF
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}';
FLUSH PRIVILEGES;
EOF

echo "🧱 Creating database and user with full privileges..."
sudo mysql -u root -p${MYSQL_ROOT_PASSWORD} <<EOF
CREATE DATABASE IF NOT EXISTS ${DB_NAME};
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "📄 Applying schema from create_device_telemetry_schema.sql..."
mysql -u root -p${MYSQL_ROOT_PASSWORD} ${DB_NAME} < "$CLONE_DIR/$SOURCE_SUBDIR/create_device_telemetry_schema.sql"


echo "📁 Creating virtualenv in $APP_DIR..."
mkdir -p $APP_DIR
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install flask flask-restx mysql-connector-python

echo "📄 Copying REST API project files from $CLONE_DIR/$SOURCE_SUBDIR..."
cp $CLONE_DIR/$SOURCE_SUBDIR/dt_RESTAPI.py $APP_DIR/
cp $CLONE_DIR/$SOURCE_SUBDIR/config.py $APP_DIR/
cp $CLONE_DIR/$SOURCE_SUBDIR/sql_queries.py $APP_DIR/
cp $CLONE_DIR/$SOURCE_SUBDIR/table_definitions.py $APP_DIR/

echo "⚙️ Creating systemd service file..."
sudo bash -c "cat > /etc/systemd/system/stack_restapi.service" <<EOF
[Unit]
Description=Stack REST API using Flask
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

echo "📡 Enabling and starting Stack REST API systemd service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable stack_restapi.service
sudo systemctl restart stack_restapi.service

echo "🔐 Configuring firewall to allow port 5000..."
sudo ufw allow OpenSSH
sudo ufw allow 5000/tcp
sudo ufw --force enable

INTERNAL_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "✅ Fresh install complete!"
echo "📍 Swagger UI available at: http://${INTERNAL_IP}:5000/"