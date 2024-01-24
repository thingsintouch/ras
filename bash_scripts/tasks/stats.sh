#!/bin/bash

# Get the cpu load 1 min and 5 min from /proc/loadavg
cpu_load_1min_percent=$(cat /proc/loadavg | awk '{print $1}')
cpu_load_5min_percent=$(cat /proc/loadavg | awk '{print $2}')
cpu_count=$(nproc)
# Get the temperature from /sys/class/thermal/thermal_zone0/temp
# Divide by 1000 to get degrees Celsius
temp_C=$(cat /sys/class/thermal/thermal_zone0/temp | awk '{print $1/1000}')
# Get the timestamp in PostgreSQL format
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
# Get the RAM usage from free command
# Divide by 1024 to get MB
used_ram_MB=$(free -m | awk 'NR==2 {print $3}')
# Get the maximal RAM available in MB
max_ram_MB=$(free -m | awk '/^Mem:/ {print $2}')
# Get the percentage of RAM that is used
# used_ram_percent=$(free -m | awk '/^Mem:/ {print $3/$2*100}')
# Round the values to integers using printf
max_ram_MB=$(printf "%.0f" $max_ram_MB)
used_ram_MB=$(printf "%.0f" $used_ram_MB)
# Round the values to integers using printf
cpu_load_1min_percent=$(bc <<< "scale=0; ($cpu_load_1min_percent*100)/$cpu_count")
cpu_load_5min_percent=$(bc <<< "scale=0; ($cpu_load_5min_percent*100)/$cpu_count")
temp_C=$(printf "%.0f" $temp_C)
used_ram_percent=$(bc <<< "scale=0; ($used_ram_MB*100)/$max_ram_MB")
# Store and print the values in stats.txt
echo "CPU load 1 min: $cpu_load_1min_percent%" 
echo "CPU load 5 min: $cpu_load_5min_percent%" 
echo "Temperature:    $temp_C°C" 
echo "Timestamp:      $timestamp" 
echo "used RAM:       $used_ram_MB MB"
echo "max RAM:        $max_ram_MB MB"
echo "used RAM:       $used_ram_percent%"
