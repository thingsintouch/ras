#!/bin/bash

# Send the POST request using curl and store the response
RESPONSE_GET_DEVICE=$(curl -s -X POST -H "$CONTENT_TYPE" -H "$SECRET_KEY" -d "$PAYLOAD_GET_DEVICE" "$URL")

# Using jq to parse the JSON object and check the length of the device list
echo "GET DEVICE RESPONSE"
echo "$RESPONSE_GET_DEVICE"

export RESPONSE_GET_DEVICE
