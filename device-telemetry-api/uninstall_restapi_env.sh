#!/bin/bash
set -e

echo "🧹 Stopping services..."
sudo systemctl stop stack_restapi.service || true
sudo systemctl disable stack_restapi.service || true

echo "🧽 Removing service and app files..."
sudo rm -f /etc/systemd/system/stack_restapi.service
sudo systemctl daemon-reload

echo "🗑️ Removing Python virtual environment..."
rm -rf $HOME/restapi-samples
echo "🗑️ samples repo"
rm -rf $HOME/samples

echo "🗑️ Removing MySQL (if needed)..."
sudo systemctl stop mysql || true
sudo apt purge -y mysql-server mysql-client mysql-common
sudo rm -rf /etc/mysql /var/lib/mysql /var/log/mysql
sudo apt autoremove -y
sudo apt autoclean

echo "🧹 Removing REST API related UFW firewall rules..."
sudo ufw delete allow 5000/tcp || true
sudo ufw delete allow 8080/tcp || true

echo "✅ All specified firewall rules removed."

echo "✅ Uninstall complete."
echo "Rebooting Now!"
# sudo reboot /y