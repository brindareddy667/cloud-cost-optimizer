# ==============================================
# Smart Cloud Cost Manager - Optimization Data Generator
# ==============================================
# Creates mock VM usage data for cost_optimization.py
# ==============================================

import pandas as pd
import numpy as np
import random

# -------------------------------
# SETTINGS
# -------------------------------
num_instances = 10  # number of VMs you want to simulate
np.random.seed(42)
random.seed(42)

# Available instance types (realistic ones)
instance_types = ['t2.micro', 't2.medium', 't2.large', 'm5.large', 'c5.large', 't3.micro']

# -------------------------------
# DATA GENERATION
# -------------------------------
data = []

for i in range(1, num_instances + 1):
    instance_id = f'VM{i}'
    instance_type = random.choice(instance_types)
    cpu_usage = np.random.randint(5, 95)             # CPU utilization %
    storage_utilization = np.random.randint(10, 95)  # Storage usage %
    hours_active = np.random.randint(8, 24)          # Active hours/day
    monthly_cost = np.random.randint(2000, 6000)     # Monthly ₹ cost

    data.append([instance_id, instance_type, cpu_usage, storage_utilization, hours_active, monthly_cost])

# -------------------------------
# SAVE TO CSV
# -------------------------------
df = pd.DataFrame(data, columns=[
    'Instance_ID',
    'Instance_Type',
    'CPU_Usage_%',
    'Storage_Utilization_%',
    'Hours_Active_per_Day',
    'Monthly_Cost'
])

df.to_csv('optimization_data.csv', index=False)

print("✅ optimization_data.csv generated successfully!\n")
print(df.head())
