#!/bin/bash
# List all python3 processes and subprocesses
pgrep -a python3 | while read pid cmd; do
  echo "Process ID: $pid"
  echo "Command: $cmd"
  echo "Subprocesses:"
  pstree -p $pid
done