#!/bin/bash
# Get the cpu load 1 min and 5 min from /proc/loadavg
cpu_load_1min=$(cat /proc/loadavg | awk '{print $1}')
cpu_load_5min=$(cat /proc/loadavg | awk '{print $2}')
cpu_count=$(nproc)
# Get the temperature from /sys/class/thermal/thermal_zone0/temp
# Divide by 1000 to get degrees Celsius
temp=$(cat /sys/class/thermal/thermal_zone0/temp | awk '{print $1/1000}')
# Get the timestamp in PostgreSQL format
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
# Get the RAM usage from free command
# Divide by 1024 to get MB
ram_usage=$(free -m | awk 'NR==2 {print $3}')
# Round the values to integers using printf
cpu_load_1min=$(bc <<< "scale=0; ($cpu_load_1min*100)/$cpu_count")
cpu_load_5min=$(bc <<< "scale=0; ($cpu_load_5min*100)/$cpu_count")
temp=$(printf "%.0f" $temp)
ram_usage=$(printf "%.0f" $ram_usage)
# Store and print the values in stats.txt
echo "CPU load 1 min: $cpu_load_1min" 
echo "CPU load 5 min: $cpu_load_5min" 
echo "Temperature: $temp°C" 
echo "Timestamp: $timestamp" 
echo "RAM usage: $ram_usage MB" 