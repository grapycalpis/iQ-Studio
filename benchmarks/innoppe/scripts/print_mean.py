# Copyright (c) 2025 Innodisk Corp.
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import csv

csv_file = "test.csv"

cpu_usage, cpu_temp, mem_usage, disk_usage, net_usage = [], [], [], [], []

def float_or_default(number,default=0.0):
    try:
        return float(number)
    except ValueError:
        return default

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cpu_usage.append(float(row['CPU Usage (%)']))
        cpu_temp.append(float_or_default(row['CPU Temperature (°C)']))
        mem_usage.append(float(row['Memory Usage (%)']))
        disk_usage.append(float(row['Disk Usage (%)']))
        net_usage.append(float(row['Network Usage (MB/s)']))

def calculate_average(data):
    return sum(data) / len(data) if data else 0

print(f"CPU Usage Average: {calculate_average(cpu_usage):.2f}%")
print(f"CPU Temperature Average: {calculate_average(cpu_temp):.2f}°C")
print(f"Memory Usage Average: {calculate_average(mem_usage):.2f}%")
print(f"Disk Usage Average: {calculate_average(disk_usage):.2f}%")
print(f"Network Usage Average: {calculate_average(net_usage):.2f} MB/s")
