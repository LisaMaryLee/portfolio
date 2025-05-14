#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status (except those explicitly overridden with `|| true`)

# --- STOP AND DISABLE SYSTEMD SERVICE ---

echo "🧹 Stopping services..."
# Stop the stack_restapi service if it's running (ignore errors if not found)
sudo systemctl stop stack_restapi.service || true
# Disable the service to prevent it from starting at boot
sudo systemctl disable stack_restapi.service || true

# --- REMOVE SERVICE FILES ---

echo "🧽 Removing service and app files..."
# Delete the systemd service unit file
sudo rm -f /etc/systemd/system/stack_restapi.service
# Reload systemd daemon to unregister the service cleanly
sudo systemctl daemon-reload

# --- DELETE VIRTUAL ENVIRONMENTS AND SAMPLES ---

echo "🗑️ Removing Python virtual environment..."
# Remove the restapi-samples directory from the user's home (where the venv likely resides)
rm -rf $HOME/restapi-samples

echo "🗑️ samples repo"
# Remove any cloned or copied sample repo contents
rm -rf $HOME/samples

# --- REMOVE MYSQL SERVER AND RELATED FILES ---

echo "🗑️ Removing MySQL (if needed)..."
# Stop the MySQL service (ignore errors if not installed)
sudo systemctl stop mysql || true
# Remove MySQL server, client, and common components
sudo apt purge -y mysql-server mysql-client mysql-common
# Delete MySQL configuration, data, and log directories
sudo rm -rf /etc/mysql /var/lib/mysql /var/log/mysql
# Clean up unused packages and residual configs
sudo apt autoremove -y
sudo apt autoclean

# --- REMOVE FIREWALL RULES (UFW) FOR PORTS USED BY REST API ---

echo "🧹 Removing REST API related UFW firewall rules..."
# Remove firewall rules for common dev/test ports
sudo ufw delete allow 5000/tcp || true
sudo ufw delete allow 8080/tcp || true

echo "✅ All specified firewall rules removed."

# --- WRAP-UP MESSAGE ---

# echo "✅ Uninstall complete."
# echo "Rebooting Now!"
# Uncomment this line to trigger a reboot after uninstall
# sudo reboot /y
