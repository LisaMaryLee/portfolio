#!/bin/bash
# setup_from_repo_restapi_ssh.sh
# This script automates installation and configuration of a Flask REST API service
# It also provisions a MySQL database and deploys helper tools for testing and viewing

set -e  # Exit immediately on error

# Git repository and application structure
REPO_SSH_URL="git@github.com:LisaMaryLee/samples.git"
APP_DIR="$HOME/restapi-telemetry"        # Target directory for Flask app
CLONE_DIR="$HOME/samples"                # Temporary clone location
SOURCE_SUBDIR="device-telemetry-api"     # Subfolder inside the repository
PYTHON_BIN="$APP_DIR/venv/bin/python"    # Python binary inside virtual environment
SCRIPT_NAME="dt_RESTAPI.py"              # Flask entry point

# Load environment variables if available
echo "📁 Loading database credentials from .env (if available)..."
if [ -f "$APP_DIR/.env" ]; then
    set -a
    source "$APP_DIR/.env"
    set +a
fi

# Fallback defaults if .env not used
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD:-ChangeThisPassword123}"
DB_NAME="${MYSQL_DB:-stack_REST}"
DB_USER="${MYSQL_USER:-1anonusage}"
DB_PASSWORD="${MYSQL_PASSWORD:-eV|76Lf/yoPZ7!3$}"

# Install core system packages
echo "🛠️ Installing required packages..."
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git curl ufw nginx mysql-server

# Clone the project repository using SSH
echo "🔐 Cloning repo using SSH..."
rm -rf $CLONE_DIR
git clone $REPO_SSH_URL $CLONE_DIR

# Ensure MySQL root account uses password-based login
echo "🔍 Checking and fixing MySQL root plugin..."
PLUGIN=$(sudo mysql -N -B --execute="SELECT plugin FROM mysql.user WHERE user='root' AND host='localhost';" 2>/dev/null || echo "auth_socket")
if [[ "$PLUGIN" != "mysql_native_password" ]]; then
    echo "🔧 Switching MySQL root auth plugin to mysql_native_password..."
    sudo mysql --execute="ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}'; FLUSH PRIVILEGES;"
else
    echo "✅ MySQL root is already using mysql_native_password."
fi

# Create the target database and user account
echo "🧱 Creating database and application user..."
mysql -u root -p${MYSQL_ROOT_PASSWORD} --execute="
CREATE DATABASE IF NOT EXISTS ${DB_NAME};
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;"

# Apply SQL schema for the telemetry tables
echo "📄 Applying schema from SQL file..."
mysql -u root -p${MYSQL_ROOT_PASSWORD} ${DB_NAME} < "$CLONE_DIR/$SOURCE_SUBDIR/create_device_telemetry_schema.sql"

# Set up a Python virtual environment for the app
echo "📁 Setting up Python virtual environment in: $APP_DIR"
mkdir -p $APP_DIR
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

# Install all required Python libraries
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install flask flask-restx mysql-connector-python faker requests tabulate flask-cors 

# Copy source code into the working directory
echo "📄 Copying Flask app and test/viewer scripts..."
cp $CLONE_DIR/$SOURCE_SUBDIR/*.py $APP_DIR/

# Create a systemd unit to run the REST API on boot
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

# Reload and enable the new systemd service
echo "📡 Enabling and starting Stack REST API service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable stack_restapi.service
sudo systemctl restart stack_restapi.service

# Configure firewall to expose required ports
echo "🔐 Configuring firewall to allow API traffic..."
sudo ufw allow OpenSSH
sudo ufw allow 5000/tcp  # REST API and Swagger UI
sudo ufw allow 8080/tcp  # HTML viewer output if needed
sudo ufw --force enable

# Get internal IP address for user output
INTERNAL_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "✅ Full setup complete!"

# Launch test data loader script
echo ""
echo "🚀 Launching test_dynamic_api_load.py for 10 entries per route..."
$PYTHON_BIN $APP_DIR/test_dynamic_api_load.py 10

# Launch database viewer
echo ""
echo "🔎 Launching view_mysql_table.py to inspect the database..."
$PYTHON_BIN $APP_DIR/view_mysql_table.py

# Show URLs to user
echo "🔎 UI to view the live database available at: http://${INTERNAL_IP}:5000/viewer"
echo "🔎 Swagger UI available at: http://${INTERNAL_IP}:5000"

echo ""
echo "🔍 Running negative test coverage..."
$PYTHON_BIN $APP_DIR/test_restapi_negative_handling.py
