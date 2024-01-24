#!/bin/bash

RAS_DIR="/home/pi/ras"
SCRIPTS_DIR="$RAS_DIR/bash_scripts"
TASKS_DIR="$SCRIPTS_DIR/tasks"
CONFIG_DIR="$SCRIPTS_DIR/config"
export RAS_DIR SCRIPTS_DIR TASKS_DIR CONFIG_DIR

# Load variables from .env file
if [ -f "$CONFIG_DIR/.env" ]; then
    source "$CONFIG_DIR/.env"
else
    source "$CONFIG_DIR/.env.example"
fi

# Define the endpoint URL
ENDPOINT_URL="$ENV_ENDPOINT_URL"

# Define the request headers
CONTENT_TYPE="$ENV_CONTENT_TYPE"
SECRET_KEY="$ENV_SECRET_KEY"

export ENDPOINT_URL
export CONTENT_TYPE
export SECRET_KEY

