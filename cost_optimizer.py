# cost_optimizer.py
import pandas as pd

def get_simple_optimizations():
    """
    Analyzes instance usage and returns simple, actionable recommendations
    and data for a savings graph with simplified text.
    """
    try:
        data = pd.read_csv('optimization_data.csv')
    except FileNotFoundError:
        return {"error": "optimization_data.csv not found."}

    optimizations = []
    suggestions = []

    # Simplify Instance IDs for display
    data['Display_ID'] = [f"VM {i+1}" for i in range(len(data))]

    for _, row in data.iterrows():
        instance_id = row['Display_ID'] # Use the new simple ID
        cpu = row['CPU_Usage_%']
        hours = row['Hours_Active_per_Day']
        current_cost = row['Monthly_Cost']
        optimized_cost = current_cost
        
        # Simple Rule 1: Right-size underutilized VMs
        if cpu < 20:
            savings = current_cost * 0.30
            optimized_cost = current_cost - savings
            suggestions.append(f"{instance_id}: CPU usage is very low ({cpu}%). Downsizing the instance could save approx. ₹{savings:,.0f}.")

        # Simple Rule 2: Schedule shutdowns for instances running 24/7
        elif hours >= 20:
            savings = current_cost * 0.25
            optimized_cost = current_cost - savings
            suggestions.append(f"{instance_id}: This instance runs 24/7. Scheduling shutdowns during off-hours could save approx. ₹{savings:,.0f}.")

        optimizations.append({
            "instance_id": instance_id, # Use the new simple ID
            "current_cost": current_cost,
            "optimized_cost": optimized_cost
        })
        
    return {
        "optimizations": optimizations,
        "suggestions": suggestions
    }