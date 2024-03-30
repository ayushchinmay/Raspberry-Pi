#!/bin/bash

echo "Raspi Hardware Benchmark Tool"
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
output_file="/home/ayush-pi/Documents/StressTests/Results/benchmark.csv"

echo "Timestamp,CPU Temperature (°C),CPU Clock Speed (MHz),CPU Throttled" > "$output_file"

echo "Idle data for 60 seconds"
for i in {1..60}; do
   timestamp=$(date +"%Y-%m-%d %H:%M:%S")
   echo "$timestamp"

   cpu_temp=$(vcgencmd measure_temp | cut -d= -f2 | cut -d\' -f1)
   echo "$cpu_temp"

   cpu_clock_speed=$(($(vcgencmd measure_clock arm | awk -F= '{print $2}') / 1000000))
   echo "$cpu_clock_speed"

   throttled_status=$(vcgencmd get_throttled)
   echo "$throttled_status"

   echo "################"
   echo "$timestamp,$cpu_temp,$cpu_clock_speed,$throttled_status" >> "$output_file"

   sleep 1
done

stress --cpu 4 -t 300 &
echo "Stress data for 300 seconds"

for i in {1..300}; do
   timestamp=$(date +"%Y-%m-%d %H:%M:%S")
   echo "$timestamp"
   cpu_temp=$(vcgencmd measure_temp | cut -d= -f2 | cut -d\' -f1)
   echo "$cpu_temp"
   cpu_clock_speed=$(($(vcgencmd measure_clock arm | awk -F= '{print $2}') / 1000000))
   echo "$cpu_clock_speed"
   throttled_status=$(vcgencmd get_throttled)
   echo "$throttled_status"
   echo "################"
   echo "$timestamp,$cpu_temp,$cpu_clock_speed,$throttled_status" >> "$output_file"
   # Sleep for 1 second
   sleep 1
done

echo "Cool down data for 60 seconds"
for i in {1..60}; do
   # Get current timestamp
   timestamp=$(date +"%Y-%m-%d %H:%M:%S")
   echo "$timestamp"
   # Get CPU temperature in degrees Celsius
   cpu_temp=$(vcgencmd measure_temp | cut -d= -f2 | cut -d\' -f1)
   echo "$cpu_temp"
   # Get CPU clock speed in MHz
   cpu_clock_speed=$(($(vcgencmd measure_clock arm | awk -F= '{print $2}') / 1000000))
   echo "$cpu_clock_speed"
   # Check if the CPU is throttled
   throttled_status=$(vcgencmd get_throttled)
   echo "$throttled_status"
   echo "################"
   # Append data to CSV file
   echo "$timestamp,$cpu_temp,$cpu_clock_speed,$throttled_status" >> "$output_file"
   # Sleep for 1 second
   sleep 1
done