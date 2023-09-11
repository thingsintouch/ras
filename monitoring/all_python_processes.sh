#!/bin/bash
# List all python3 subprocesses without full path
pgrep -a python3 | while read pid cmd; do
  basename "$cmd" | xargs pstree -a -p $pid
done | tr '\n' ';' | sed 's/;;/;/g'