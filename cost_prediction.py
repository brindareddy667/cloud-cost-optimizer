# cost_prediction.py
import pandas as pd

# Load the pricing data from the CSV file when the script starts
try:
    pricing_df = pd.read_csv('instance_pricing.csv')
except FileNotFoundError:
    print("FATAL ERROR: instance_pricing.csv not found. The calculator will not work.")
    pricing_df = pd.DataFrame() # Create an empty dataframe to avoid crashing

def calculate_cost_from_params(vm_count, instance_type, usage_hours, currency):
    """
    Calculates cost by looking up prices from the instance_pricing.csv file.
    """
    if pricing_df.empty:
        return 0 # Return 0 if the pricing data failed to load

    # --- 1. Find the correct price from the CSV ---
    # The frontend doesn't send the region code, but we can get it from the currency
    # This is a simple mapping for our example
    region_map = {
        'USD': 'us-central1',
        'INR': 'asia-south1',
        'EUR': 'europe-west3'
    }
    region_code = region_map.get(currency, 'us-central1')

    # Filter the dataframe to find the specific row for the instance and region
    matched_instance = pricing_df[
        (pricing_df['instance_type'] == instance_type) & 
        (pricing_df['region_code'] == region_code)
    ]

    if matched_instance.empty:
        return 0 # Return 0 if no price was found

    cost_per_hour_usd = matched_instance.iloc[0]['cost_per_hour_usd']

    # --- 2. Perform the calculation in USD ---
    total_cost_usd = vm_count * cost_per_hour_usd * usage_hours

    # --- 3. Convert to the user's selected currency ---
    conversion_rates = {'USD_TO_INR': 83.50, 'USD_TO_EUR': 0.92}
    final_cost = total_cost_usd

    if currency == 'INR':
        final_cost = total_cost_usd * conversion_rates['USD_TO_INR']
    elif currency == 'EUR':
        final_cost = total_cost_usd * conversion_rates['USD_TO_EUR']
        
    return final_cost