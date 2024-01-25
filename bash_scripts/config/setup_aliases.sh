#!/bin/bash

# Define a function that performs the desired action

setup_aliases() {
    alias startras='bash $TASKS_DIR/startras.sh'
    alias stopras='bash $TASKS_DIR/stopras.sh'
    alias allalive='source $TASKS_DIR/all_alive_boolean.sh'
    alias stats='source $TASKS_DIR/stats.sh'
    alias fepu='source $TASKS_DIR/update_repo.sh'
    alias conmo='source $SCRIPTS_DIR/config/config_monitoring.sh'
    alias bootparams='source $TASKS_DIR/boot_params.sh'
    alias create_boot_payloads='source $TASKS_DIR/create_boot_payloads.sh'
    alias post_get_device='source $TASKS_DIR/post_get_device.sh'
}
# Call the function to set up aliases
setup_aliases

# Rest of your script
echo "Aliases defined..."