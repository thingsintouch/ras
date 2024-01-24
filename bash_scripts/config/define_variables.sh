#!/bin/bash

# Load variables from .env file
if [ -f "$(dirname "$0")/.env" ]; then
    source "$(dirname "$0")/.env"
fi


RAS_DIR="/home/pi/ras"
export RAS_DIR

SCRIPTS_DIR="$RAS_DIR/bash_scripts"
export SCRIPTS_DIR

TASKS_DIR="$SCRIPTS_DIR/tasks"
export TASKS_DIR

# Define the endpoint URL
ENDPOINT_URL="$ENV__ENDPOINT_URL"

# Define the request headers
CONTENT_TYPE="$ENV__CONTENT_TYPE"
SECRET_KEY="$ENV__SECRET_KEY"

export ENDPOINT_URL
export CONTENT_TYPE
export SECRET_KEY

