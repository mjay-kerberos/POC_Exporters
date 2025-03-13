#!/bin/bash

# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install dependencies from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# Specify the Go version and URL
GO_VERSION="go1.24.1"
GO_URL="https://go.dev/dl/${GO_VERSION}.linux-amd64.tar.gz"

# Download and install Go
wget ${GO_URL} -O ${GO_VERSION}.linux-amd64.tar.gz || { echo "Failed to download Go"; exit 1; }
sudo tar -C /usr/local -xzf ${GO_VERSION}.linux-amd64.tar.gz
rm ${GO_VERSION}.linux-amd64.tar.gz

# Add Go to PATH
echo "export PATH=\$PATH:/usr/local/go/bin" >> ~/.bashrc
source ~/.bashrc

echo "Go ${GO_VERSION} installation completed successfully!"
