#!/bin/bash

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get -y install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings

# Check if the docker GPG key already exists
if [ ! -f /etc/apt/keyrings/docker.gpg ]; then
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
fi

sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package manager
sudo apt-get update

# install docker and friends
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# upadte docker socket permissions
sudo chmod 666 /var/run/docker.sock

# set build directory from current working directory
export BUILD_DIRECTORY="$PWD"

# Create a systemd service unit file for your Python script
cat <<EOF | sudo tee /etc/systemd/system/favicon-fetcher.service
[Unit]
Description=Favicon Fetching API Service
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=unless-stopped
EnvironmentFile=/etc/my_service_env.conf
WorkingDirectory=$BUILD_DIRECTORY
ExecStart=/usr/bin/docker compose up --build

[Install]
WantedBy=multi-user.target
EOF

# Reload the systemd daemon to recognize the new service
sudo systemctl daemon-reload

# Start the service
sudo systemctl start favicon-fetcher.service

# Enable the service to start on boot
sudo systemctl enable favicon-fetcher.service