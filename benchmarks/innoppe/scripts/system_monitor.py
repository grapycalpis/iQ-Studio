# Copyright (c) 2025 Innodisk Corp.
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import psutil
import time
import csv
from datetime import datetime

PERIOD = 1

# CSV file name
CSV_FILE = "test.csv"

# CSV column names
FIELDS = ["Timestamp", "CPU Usage (%)", "CPU Temperature (°C)", "Memory Usage (%)", "Disk Usage (%)", "Network Usage (MB/s)"]

# Create or overwrite the CSV file and write the header
with open(CSV_FILE, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(FIELDS)  # Write the header

print(f"Created new file: {CSV_FILE}")

# Start logging system metrics
while True:
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Get CPU temperature
    temps = psutil.sensors_temperatures()
    cpu_temp = None

    if 'coretemp' in temps:  
        for sensor in temps['coretemp']:  
            if sensor.label == 'Package id 0':  
                cpu_temp = sensor.current
                break

    # Get memory usage
    memory_usage = psutil.virtual_memory().percent
    
    # Calculate network usage (difference over 1 second)
    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()
    net_usage = round(((net2.bytes_sent + net2.bytes_recv) - (net1.bytes_sent + net1.bytes_recv)) / (1024 * 1024) * 100) / 100  # MB/s
    
    # Get disk free space percentage
    disk_free = round((psutil.disk_usage("/").total-psutil.disk_usage("/").free) / psutil.disk_usage("/").total * 100 * 100) / 100  # Percentage

    # Append data to the CSV file
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, cpu_usage, cpu_temp, memory_usage, disk_free, net_usage])
    
    # print(f"Logged: {timestamp}, CPU: {cpu_usage}%, Memory: {memory_usage}%, Disk Free: {disk_free:.2f}%, Network: {net_usage:.2f}MB/s")
    
    # Wait for 4 more seconds to maintain a 5-second interval
    time.sleep(PERIOD)
