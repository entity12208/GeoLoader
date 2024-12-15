#!/bin/bash

# GeoLoader installation script

# Set the installation directory
INSTALL_DIR="$HOME/GeoLoader"

# Check if the script is being run with root privileges
if [ "$(id -u)" != "0" ]; then
    echo "Please run as root or use sudo"
    exit 1
fi

# Install required dependencies
echo "Installing dependencies..."
sudo apt update
sudo apt upgrade
sudo apt install -y build-essential git python3 python3-pip cmake
pip install --upgrade-pip
# Clone the GeoLoader repository
echo "Cloning GeoLoader repository..."
git clone https://github.com/entity12208/GeoLoader.git $INSTALL_DIR

# Navigate to the GeoLoader directory
cd $INSTALL_DIR

# Set up Python virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Build GeoLoader
echo "Building GeoLoader..."
cd scripts
sudo chmod +x build.sh
./build.sh

echo "GeoLoader installed successfully at $INSTALL_DIR"
echo "You can now run GeoLoader using './geoloader' or create mods using '.gloader' files."
