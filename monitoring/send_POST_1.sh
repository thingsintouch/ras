#!/bin/bash

# Define the endpoint URL
URL="https://2309a_hasura.thingserp.com/v1/graphql"

# Define the request headers
CONTENT_TYPE="content-type: application/json"
SECRET_KEY="x-hasura-admin-secret: myadminsecretkey"

CUSTOMER="this is getting interesting"

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
import json

# Define the path to the JSON file
JSON_FILE = '/home/pi/ras/factory_settings/custom_params.json'

try:
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
        production_number = data.get('productionNumber', 'not defined')
        print(str(production_number))
except FileNotFoundError:
    print(f'File {JSON_FILE} not found.')
except json.JSONDecodeError:
    print(f'Error decoding JSON in {JSON_FILE}.')
"

# Run the Python script and capture its output
PRODUCTION_NUMBER=$(python3 -c "$PYTHON_SCRIPT")
fi

# Define the mutation JSON payload
# Use a heredoc to define it
read -r -d '' PAYLOAD <<EOF
{
  "query": "mutation NewRAS2 {
    insert_device_one(object: {
      Customer: \"$CUSTOMER\",
      MAC_eth0: \"$MAC_ETH0\",
      MAC_wlan0: \"$MAC_WLAN0\",
      Machine_ID: \"$MACHINE_ID\",
      Production_Number: \"$PRODUCTION_NUMBER\"
    }) {
      id
    }
  }"
}
EOF

# Remove newline characters from PAYLOAD
PAYLOAD=$(echo "$PAYLOAD" | tr -d '\n')

# Send the POST request using curl and store the response
RESPONSE=$(curl -s -X POST -H "$CONTENT_TYPE" -H "$SECRET_KEY" -d "$PAYLOAD" "$URL")

# Print the response
echo "$RESPONSE"
