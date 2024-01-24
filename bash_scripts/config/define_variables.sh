#!/bin/bash

# Get the directory of the current script
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load variables from .env file
if [ -f "$CURRENT_DIR/.env" ]; then
    source "$CURRENT_DIR/.env"
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

