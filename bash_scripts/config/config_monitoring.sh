#!/bin/bash

# Get the directory of the current script
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "$CURRENT_DIR/define_variables.sh"
source "$CURRENT_DIR/setup_aliases.sh"

# get the boot parameters into environment variables
bootparams
#create the payloads needed to send the boot params to db
create_boot_payloads