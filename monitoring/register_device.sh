#!/bin/bash

# Check if jq is installed
if command -v jq &> /dev/null
then
    echo "jq is installed"
else
    echo "jq is not installed, installing it now"
    # Install jq using apt
    sudo apt update
    sudo DEBIAN_FRONTEND=noninteractive apt install -y jq
fi

# Define the endpoint URL
URL="https://2309a_hasura.thingserp.com/v1/graphql"

# Define the request headers
CONTENT_TYPE="content-type: application/json"
SECRET_KEY="x-hasura-admin-secret: myadminsecretkey"

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


# Define the query JSON payload to see if the device exists in the database
# Use a heredoc to define it
read -r -d '' PAYLOAD_GET_DEVICE <<EOF
{
    "query": "query GetDevice {
    device(where: {Machine_ID: {_eq:  \"$MACHINE_ID\"}}) {
        id
        Machine_ID
        MAC_wlan0
        MAC_eth0
        Customer
        Production_Number
    }
    }"
}
EOF

# Define the mutation JSON payload to create a new register for thedevice
# Use a heredoc to define it
read -r -d '' PAYLOAD_CREATE_NEW_DEVICE <<EOF
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

# Define the query JSON payload to see if the device exists in the database
# Use a heredoc to define it
read -r -d '' PAYLOAD_UPDATE_DEVICE <<EOF
{
    "query": "mutation InsertDevice {
        update_device(where: {Machine_ID: {_eq:  \"$MACHINE_ID\"}},
            _set: { MAC_eth0: \"$MAC_ETH0\",
            MAC_wlan0: \"$MAC_WLAN0\"})
            {
                returning {
                    id
                    Machine_ID
                    MAC_wlan0
                    MAC_eth0
                    Customer
                    Production_Number
                }
            }   
        }"
}
EOF

# Remove newline characters from PAYLOAD
PAYLOAD_CREATE_NEW_DEVICE=$(echo "$PAYLOAD_CREATE_NEW_DEVICE" | tr -d '\n')
PAYLOAD_GET_DEVICE=$(echo "$PAYLOAD_GET_DEVICE" | tr -d '\n')
PAYLOAD_UPDATE_DEVICE=$(echo "$PAYLOAD_UPDATE_DEVICE" | tr -d '\n')
#echo $PAYLOAD_GET_DEVICE
#echo $PAYLOAD_UPDATE_DEVICE

# Send the POST request using curl and store the response
RESPONSE=$(curl -s -X POST -H "$CONTENT_TYPE" -H "$SECRET_KEY" -d "$PAYLOAD_GET_DEVICE" "$URL")

# Using jq to parse the JSON object and check the length of the device list
# echo "$RESPONSE"

DEVICE_IN_DB=$(echo "$RESPONSE" | jq '.data.device | length')

if [ $DEVICE_IN_DB -gt 0 ]; then
    #the device exists in the database
    HAS_DEVICE=true
    # Send the POST request to create a new record in the db for the device
    RESPONSE=$(curl -s -X POST -H "$CONTENT_TYPE" -H "$SECRET_KEY" -d "$PAYLOAD_UPDATE_DEVICE" "$URL")
    #echo "$RESPONSE"    
else
    #the device does not exist in the database
    HAS_DEVICE=false
    # Send the POST request to create a new record in the db for the device
    RESPONSE=$(curl -s -X POST -H "$CONTENT_TYPE" -H "$SECRET_KEY" -d "$PAYLOAD_CREATE_NEW_DEVICE" "$URL")
    #echo "$RESPONSE"

fi

# Printing the value of the boolean variable
#echo "HAS_DEVICE=$HAS_DEVICE"
