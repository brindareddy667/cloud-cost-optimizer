# ==============================================
# Smart Cloud Cost Manager - Dataset Generator
# ==============================================
# Generates mock usage data for the cost prediction model.
# You can control how many months of data you want.
# ==============================================

import pandas as pd
import numpy as np

# ----- PARAMETERS -----
num_records = 12  # number of months (you can change this)
np.random.seed(42)  # for consistent results

# ----- GENERATE MOCK DATA -----
usage_hours = np.arange(100, 100 + num_records * 10, 10)  # e.g., 100,110,...220
base_cost_per_hour = 15  # ₹ per usage hour

# Random variation (to make it look realistic)
random_factor = np.random.uniform(0.9, 1.1, num_records)

cost = usage_hours * base_cost_per_hour * random_factor

# Create DataFrame
data = pd.DataFrame({
    'Month': [f'Month_{i+1}' for i in range(num_records)],
    'Usage_Hours': usage_hours,
    'Cost': cost.round(2)
})

# ----- SAVE TO CSV -----
data.to_csv('usage_data.csv', index=False)
print("✅ Dataset generated successfully: usage_data.csv")
print(data.head())
