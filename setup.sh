#!/bin/bash

# Update package list
sudo apt update

# Install Python 3 & pip3
sudo apt install -y python3
sudo apt install -y python3-pip

# Install Python packages from requirements.txt
pip3 install -r requirements.txt

# Run your Python script (replace script.py with your script's name)
# python3 ff.py

# Create a systemd service unit file for your Python script
cat <<EOF | sudo tee /etc/systemd/system/faviconfetcher.service
[Unit]
Description=Favicon Fetch API Service
After=network.target

[Service]
User=azureuser
ExecStart=/usr/bin/python3 /home/azureuser/project3-1.0.0/favfetch.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to read the new service unit file
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable faviconfetcher
sudo systemctl start faviconfetcher
journalctl -u faviconfetcher -f