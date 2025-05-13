#!/bin/bash
# setup_from_repo_restapi_ssh.sh
# This script automates the setup of a Flask-based REST API with MySQL backend and dynamic viewer.

set -e  # Exit immediately if any command fails

# Repository and project paths
REPO_SSH_URL="git@github.com:LisaMaryLee/samples.git"
APP_DIR="$HOME/restapi-telemetry"        # Final destination for app files
CLONE_DIR="$HOME/samples"                # Temporary location to clone repo
SOURCE_SUBDIR="device-telemetry-api"     # Folder inside repo containing source code
PYTHON_BIN="$APP_DIR/venv/bin/python"    # Path to Python inside virtual environment
SCRIPT_NAME="dt_RESTAPI.py"              # Flask app entry point

# MySQL credentials
MYSQL_ROOT_PASSWORD="ChangeThisPassword123"
DB_NAME="stack_REST"
DB_USER="1anonusage"
DB_PASSWORD="eV|76Lf/yoPZ7!3$"

# Install required system packages
echo "🛠️ Installing required packages..."
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git curl ufw nginx mysql-server

# Clone the Git repository via SSH
echo "🔐 Cloning repo using SSH..."
rm -rf $CLONE_DIR
git clone $REPO_SSH_URL $CLONE_DIR

# Check and update MySQL root plugin if necessary
echo "🔍 Checking and fixing MySQL root plugin..."
PLUGIN=$(sudo mysql -N -B --execute="SELECT plugin FROM mysql.user WHERE user='root' AND host='localhost';" 2>/dev/null || echo "auth_socket")
if [[ "$PLUGIN" != "mysql_native_password" ]]; then
    echo "🔧 Switching MySQL root auth plugin to mysql_native_password..."
    sudo mysql --execute="ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}'; FLUSH PRIVILEGES;"
else
    echo "✅ MySQL root is already using mysql_native_password."
fi

# Create application database and user
echo "🧱 Creating database and application user..."
mysql -u root -p${MYSQL_ROOT_PASSWORD} --execute="
CREATE DATABASE IF NOT EXISTS ${DB_NAME};
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;"

# Apply schema to database
echo "📄 Applying schema from SQL file..."
mysql -u root -p${MYSQL_ROOT_PASSWORD} ${DB_NAME} < "$CLONE_DIR/$SOURCE_SUBDIR/create_device_telemetry_schema.sql"

# Set up virtual environment for Python dependencies
echo "📁 Setting up Python virtual environment in: $APP_DIR"
mkdir -p $APP_DIR
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install flask flask-restx mysql-connector-python faker requests tabulate

# Copy application and support scripts
echo "📄 Copying Flask app and test/viewer scripts..."
cp $CLONE_DIR/$SOURCE_SUBDIR/*.py $APP_DIR/

# Create systemd service for the Flask REST API
echo "⚙️ Creating systemd service for the REST API..."
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

# Enable and start the systemd service
echo "📡 Enabling and starting Stack REST API service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable stack_restapi.service
sudo systemctl restart stack_restapi.service

# Open necessary ports through UFW firewall
echo "🔐 Configuring firewall to allow API traffic..."
sudo ufw allow OpenSSH
sudo ufw allow 5000/tcp  # For REST API and Swagger UI
sudo ufw allow 8080/tcp  # Reserved for local web viewer if used
sudo ufw --force enable

# Show IP address of the system
INTERNAL_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "✅ Full setup complete!"

# Run test data loader
echo ""
echo "🚀 Launching test_dynamic_api_load.py for 10 entries per route..."
$PYTHON_BIN $APP_DIR/test_dynamic_api_load.py 10

# Launch terminal-based MySQL viewer
echo ""
echo "🔎 Launching view_mysql_table.py to inspect the database..."
$PYTHON_BIN $APP_DIR/view_mysql_table.py

# Show endpoints
echo "🔎 UI to view the live database available at: http://${INTERNAL_IP}:5000/viewer"
echo "🔎 Swagger UI available at: http://${INTERNAL_IP}:5000"
