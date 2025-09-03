# Copyright (c) 2025 Innodisk Corp.
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt

INPUT_CSV = "test.csv"

OUTPUT_FOLDER = "reports/"
OUTPUT_CPU_SEPARATE_PNG = "system_usage_cpu_separate.png"
OUTPUT_CPU_COMBINE_PNG = "system_usage_cpu_combine.png"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Read the CSV file
df = pd.read_csv(INPUT_CSV, parse_dates=["Timestamp"])

# Set timestamp as index
df.set_index("Timestamp", inplace=True)

####################################################  CPU Separate (without temperature)  ####################################################
# Plot four graphs
# metrics = ["CPU Usage (%)", "Memory Usage (%)", "Disk Usage (%)", "Network Usage (MB/s)"]
# fig, axes = plt.subplots(4, 1, figsize=(10, 12))

# for i, metric in enumerate(metrics):
#     axes[i].plot(df.index, df[metric], marker="o", linestyle="-", label=metric)
#     axes[i].set_xlabel("Time")
#     axes[i].set_ylabel(metric)
#     axes[i].legend()
#     axes[i].grid()

# plt.tight_layout()
# plt.savefig(OUTPUT_FOLDER + OUTPUT_CPU_SEPARATE_PNG)

####################################################  CPU Separate  ####################################################
# Plot four graphs
metrics = ["CPU Usage (%)", "CPU Temperature (°C)", "Memory Usage (%)", "Disk Usage (%)", "Network Usage (MB/s)"]
fig, axes = plt.subplots(5, 1, figsize=(10, 12))

for i, metric in enumerate(metrics):
    axes[i].plot(df.index, df[metric], marker="o", linestyle="-", label=metric)
    axes[i].set_xlabel("Time")
    axes[i].set_ylabel(metric)
    axes[i].legend()
    axes[i].grid()

plt.tight_layout()
plt.savefig(OUTPUT_FOLDER + OUTPUT_CPU_SEPARATE_PNG)


####################################################  CPU Combine  ####################################################
# Plot graphs
fig, axes = plt.subplots(4, 1, figsize=(10, 12))

# CPU Usage and Temperature in one plot
ax1 = axes[0]
ax2 = ax1.twinx()  # Create a secondary y-axis

ax1.plot(df.index, df["CPU Usage (%)"], marker="o", linestyle="-", color="b", label="CPU Usage (%)")
ax2.plot(df.index, df["CPU Temperature (°C)"], marker="s", linestyle="--", color="r", label="CPU Temp (°C)")

ax1.set_xlabel("Time")
ax1.set_ylabel("CPU Usage (%)", color="b")
ax2.set_ylabel("CPU Temperature (°C)", color="r")

ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
ax1.grid()

# Other metrics
metrics = ["Memory Usage (%)", "Disk Usage (%)", "Network Usage (MB/s)"]
for i, metric in enumerate(metrics):
    axes[i + 1].plot(df.index, df[metric], marker="o", linestyle="-", label=metric)
    axes[i + 1].set_xlabel("Time")
    axes[i + 1].set_ylabel(metric)
    axes[i + 1].legend()
    axes[i + 1].grid()

plt.tight_layout()
plt.savefig(OUTPUT_FOLDER + OUTPUT_CPU_COMBINE_PNG)
