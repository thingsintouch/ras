#!/bin/bash
# List all python3 subprocesses without full path
pgrep -a python3 | while read pid cmd; do
  # Check if the process is still running
  if kill -0 $pid 2>/dev/null; then
    # Remove the path from the command name using cut
    cmd=$(echo "$cmd" | cut -d' ' -f1 | cut -d'/' -f5)
    # Call pstree with the command name
    pstree -a -p $pid "$cmd"
  fi
done | tr '\n' ';' | sed 's/;;/;/g'