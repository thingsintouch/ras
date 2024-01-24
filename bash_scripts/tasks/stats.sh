#!/bin/bash
# Get the cpu load 1 min and 5 min from /proc/loadavg
CPU_LOAD_1MIN_PERCENT=$(cat /proc/loadavg | awk '{print $1}')
CPU_LOAD_5MIN_PERCENT=$(cat /proc/loadavg | awk '{print $2}')
cpu_count=$(nproc)
# Get the temperature from /sys/class/thermal/thermal_zone0/temp
# Divide by 1000 to get degrees Celsius
TEMP_C=$(cat /sys/class/thermal/thermal_zone0/temp | awk '{print $1/1000}')
# Get the TIMESTAMP in PostgreSQL format
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
# Get the RAM usage from free command
# Divide by 1024 to get MB
USED_RAM_MB=$(free -m | awk 'NR==2 {print $3}')
# Get the maximal RAM available in MB
MAX_RAM_MB=$(free -m | awk '/^Mem:/ {print $2}')
# Get the percentage of RAM that is used
# USED_RAM_PERCENT=$(free -m | awk '/^Mem:/ {print $3/$2*100}')
# Round the values to integers using printf
MAX_RAM_MB=$(printf "%.0f" $MAX_RAM_MB)
USED_RAM_MB=$(printf "%.0f" $USED_RAM_MB)
# Round the values to integers using printf
CPU_LOAD_1MIN_PERCENT=$(bc <<< "scale=0; ($CPU_LOAD_1MIN_PERCENT*100)/$cpu_count")
CPU_LOAD_5MIN_PERCENT=$(bc <<< "scale=0; ($CPU_LOAD_5MIN_PERCENT*100)/$cpu_count")
TEMP_C=$(printf "%.0f" $TEMP_C)
USED_RAM_PERCENT=$(bc <<< "scale=0; ($USED_RAM_MB*100)/$MAX_RAM_MB")
# Store and print the values in stats.txt
echo "CPU load 1 min: $CPU_LOAD_1MIN_PERCENT%" 
echo "CPU load 5 min: $CPU_LOAD_5MIN_PERCENT%" 
echo "Temperature:    $TEMP_C°C" 
echo "TIMESTAMP:      $TIMESTAMP" 
echo "used RAM:       $USED_RAM_MB MB"
echo "max RAM:        $MAX_RAM_MB MB"
echo "used RAM:       $USED_RAM_PERCENT%"

export CPU_LOAD_1MIN_PERCENT
export CPU_LOAD_5MIN_PERCENT
export TEMP_C
export TIMESTAMP
export USED_RAM_MB
export MAX_RAM_MB
export USED_RAM_PERCENT