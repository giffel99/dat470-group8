#!/bin/bash

# Cores is number of cores per socket multiplied with the number of sockets
cores_per_socket=$(lscpu | grep "Core(s) per socket" | grep -Eo '[0-9]+')
sockets=$(lscpu | grep "Socket(s)" | grep -Eo '[0-9]+')

num_cores=$((cores_per_socket*sockets))


# Get the type of CPUs and clock frequency
cpu_info=$(lscpu | grep 'Model name' | awk -F: '{$1="";print}' | awk '{$1=$1;print}')
cpu_clock_low=$( cat /proc/cpuinfo | grep 'cpu MHz' | sort | head -n 1 | awk -F: '{$1="";print}')
cpu_clock_high=$( cat /proc/cpuinfo | grep 'cpu MHz' | sort | tail -n 1 | awk -F: '{$1="";print}')

# Get disk usage and total available for the filesystems /data and /datainbackup
disk_usage_data=$(df -h --output=used,size /data | tail -n 1)
disk_usage_datainbackup=$(df -h --output=used,size /datainbackup | tail -n 1)


# Get memory usage of current login shell
shell_pid=$$
shell_mem_usage=$(pmap $shell_pid | tail -n 1 | awk '{print $2}')


# Print all the information gathered
echo "1. Number of cores: $num_cores (with HyperThreading)"
echo "2. Type of CPU: $cpu_info"
echo "3. Clock frequencies (cpu MHz) between: $cpu_clock_low   - $cpu_clock_high"
echo "4. Disk usage (used, total):"
echo "   /data: $disk_usage_data"
echo "   /datainbackup: $disk_usage_datainbackup"
echo "5. Memory usage of login shell: ${shell_mem_usage}KB"

