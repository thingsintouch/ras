#!/bin/bash

# Function to check if alias is defined
alias_is_defined() {
    alias "$1" &>/dev/null
}

# Check if 'startras' alias is defined
if ! alias_is_defined 'startras'; then
    echo "alias startras='bash /home/pi/ras/bash_scripts/startras.sh'" >> ~/.bashrc
fi

# Check if 'stopras' alias is defined
if ! alias_is_defined 'stopras'; then
    echo "alias startras='bash /home/pi/ras/bash_scripts/startras.sh'" >> ~/.bashrc
fi

source ~/.bashrc
