#!/bin/bash
# List all python3 processes and subprocesses
output=$(pgrep -a python3 | while read pid cmd; do
  #echo "Process ID: $pid"
  #echo "Command: $cmd"
  #echo "Subprocesses:"
  pstree -p $pid
done | tr '\n' ';' | sed 's/;;/;/g' | tr -d ' ')

# Print the output
echo "$output"

# Declare boolean variables and initialize them to false
declare -A bool_vars=( [bluetooth]=false [buzzer]=false [clock]=false [display]=false [odoo.]=false [reader]=false [setup_server]=false [RegisterClo]=false [state]=false [thermal]=false )

# Loop through the keys of the associative array
for key in "${!bool_vars[@]}"; do
  # Test if the output contains the key using grep
  if echo "$output" | grep -q "$key"; then
    # Set the value of the variable to true
    bool_vars[$key]=true
  fi
done

# Print the values of the boolean variables
for key in "${!bool_vars[@]}"; do
  echo "$key: ${bool_vars[$key]}"
done
