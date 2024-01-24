#!/bin/bash



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

export PAYLOAD_CREATE_NEW_DEVICE
export PAYLOAD_GET_DEVICE
export PAYLOAD_UPDATE_DEVICE
