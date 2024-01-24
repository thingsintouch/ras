#!/bin/bash

# Define a function that performs the desired action
setup_aliases() {
    alias startras='bash /home/pi/ras/bash_scripts/startras.sh'
    alias stopras='bash /home/pi/ras/bash_scripts/stopras.sh'
    alias allalive='$SCRIPTS_DIR/tasks/all_alive_boolean.sh'

# Call the function to set up aliases
setup_aliases

# Rest of your script
echo "Aliases defined..."