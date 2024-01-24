#!/bin/bash

CUSTOMER="not defined"

# Get the Machine ID
MACHINE_ID=$(cat /etc/machine-id)

# Get the MAC address of wlan0
MAC_WLAN0=$(ifconfig wlan0 | awk '/ether/{print $2}')

# Get the MAC address of eth0
MAC_ETH0=$(ifconfig eth0 | awk '/ether/{print $2}')

# Define the Python file path
PYTHON_FILE="/home/pi/ras/factory_settings/custom_params.py"

# Initialize the variable with a default value
PRODUCTION_NUMBER="not defined"

# Check if the Python file exists
if [ -f "$PYTHON_FILE" ]; then
# Define the Python script
PYTHON_SCRIPT="
PYTHON_FILE = '/home/pi/ras/factory_settings/custom_params.py'

try:
    with open(PYTHON_FILE, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'productionNumber' in line:
                production_number = line.split('\"')[-2]
                print(f'{production_number}')
                break
        else:
            print('Production Number not found.')
except FileNotFoundError:
    print(f'File {PYTHON_FILE} not found.')
"

# Run the Python script and capture its output
PRODUCTION_NUMBER=$(python3 -c "$PYTHON_SCRIPT")
fi

# Navigate to the Git repository directory
cd $RAS_DIR

# Get the current Git branch
GIT_BRANCH=$(git symbolic-ref --short HEAD)

# Get the current Git commit hash
GIT_TAG=$(git describe --tags)
GIT_HASH=$(git rev-parse --short origin/$GIT_BRANCH)

# Get the remote repository URL (assuming there's only one remote named "origin")
GIT_REPOSITORY=$(git config --get remote.origin.url)

echo "GIT_BRANCH=$GIT_BRANCH" 
echo "GIT_TAG=$GIT_TAG"
echo "GIT_HASH=$GIT_HASH"
echo "GIT_REPOSITORY='$GIT_REPOSITORY'"

# Get the boot duration using systemd-analyze and convert it to milliseconds
BOOT_TIME=$(systemd-analyze | grep "Startup finished" | awk -F'= ' '{print $2}')

# Print the boot duration in milliseconds
echo "Last boot took approximately $BOOT_TIME"

export CUSTOMER MACHINE_ID MAC_WLAN0 MAC_ETH0 PRODUCTION_NUMBER
export GIT_BRANCH GIT_TAG GIT_HASH GIT_REPOSITORY BOOT_TIME