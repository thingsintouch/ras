#!/bin/bash

# Define a function that performs the desired action

setup_aliases() {
    alias startras='bash $TASKS_DIR/startras.sh'
    alias stopras='bash $TASKS_DIR/stopras.sh'
    alias allalive='source $TASKS_DIR/all_alive_boolean.sh'
    alias stats='source $TASKS_DIR/stats.sh'
    alias fepu='source $TASKS_DIR/update_repo.sh'
}
# Call the function to set up aliases
setup_aliases

# Rest of your script
echo "Aliases defined..."