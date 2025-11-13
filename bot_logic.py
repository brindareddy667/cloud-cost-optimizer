# bot_logic.py
import json
import re

def load_provider_data():
    try:
        with open('provider_data.json', 'r') as file: return json.load(file)
    except FileNotFoundError: return None

def calculate_cost(service, service_type, usage):
    conversion_rate = 85
    if service_type in ["compute", "database"]: return service["cost_per_hour"] * usage * conversion_rate
    elif service_type == "storage": return service["cost_per_gb"] * usage * conversion_rate
    return 0

# (get_simple_recommendation function is unchanged)
def get_simple_recommendation(service_type, usage, budget, priority):
    provider_data = load_provider_data()
    if not provider_data: return {"error": "provider_data.json not found."}
    services = provider_data.get(service_type, [])
    results = []
    for s in services:
        total_cost = calculate_cost(s, service_type, usage)
        score = (10 - (total_cost / budget) * 5) + s["performance"]
        results.append({ "provider": s["provider"], "service": s["service"], "total_cost": total_cost, "performance": s["performance"], "score": score })
    if priority == "cost": results.sort(key=lambda x: x["total_cost"])
    elif priority == "performance": results.sort(key=lambda x: x["performance"], reverse=True)
    else: results.sort(key=lambda x: x["score"], reverse=True)
    return {"recommendations": results[:3]}

# --- NEW PRO BOT LOGIC: The Architecture Advisor ---
def get_architecture_recommendation(project_description):
    provider_data = load_provider_data()
    project_description = project_description.lower()
    recommendations = []
    
    # Keyword-based service detection
    if any(keyword in project_description for keyword in ["website", "blog", "app", "server"]):
        # Find the best value compute service (e.g., highest performance for the lowest cost)
        compute_options = provider_data.get('compute', [])
        best_compute = min(compute_options, key=lambda x: x['cost_per_hour'] / x['performance'])
        recommendations.append(f"**Compute:** For your web host, I recommend **{best_compute['provider']} - {best_compute['service']}**. It offers the best balance of cost and performance.")

    if any(keyword in project_description for keyword in ["database", "user data", "products"]):
        db_options = provider_data.get('database', [])
        best_db = min(db_options, key=lambda x: x['cost_per_hour'] / x['performance'])
        recommendations.append(f"**Database:** To store your data, **{best_db['provider']} - {best_db['service']}** is a reliable and cost-effective choice.")

    if any(keyword in project_description for keyword in ["images", "storage", "files", "videos"]):
        storage_options = provider_data.get('storage', [])
        best_storage = min(storage_options, key=lambda x: x['cost_per_gb'] / x['performance'])
        recommendations.append(f"**Storage:** For file and image hosting, **{best_storage['provider']} - {best_storage['service']}** is highly recommended.")
        
    if not recommendations:
        return "I can help design an architecture. Please describe your project, for example: 'I am building an e-commerce website with a user database and image storage.'"
    
    # Format the final reply
    reply = "Based on your project description, here is a recommended cloud architecture:\n\n- " + "\n- ".join(recommendations)
    return reply

# (get_chat_response for the simple chatbot is unchanged)
def get_chat_response(user_message):
    # ... (function is unchanged)
    provider_data = load_provider_data()
    if not provider_data: return "Sorry, my data file seems to be missing."
    user_message = user_message.lower()
    if any(word in user_message for word in ["hello", "hi", "hey"]): return "Hello! I'm the Cloud Selector Bot. How can I help you find a service today?"
    service_type, usage, budget, priority = None, None, None, "balanced"
    if 'compute' in user_message: service_type = 'compute'
    elif 'storage' in user_message: service_type = 'storage'
    elif 'database' in user_message: service_type = 'database'
    numbers = [float(n) for n in re.findall(r'(\d+\.?\d*)', user_message)]
    if len(numbers) >= 2: usage, budget = numbers[0], numbers[1]
    elif len(numbers) == 1: usage = numbers[0]
    if any(word in user_message for word in ['₹', 'rs', 'rupee', 'budget']):
        if not budget: budget = usage
    if 'cost' in user_message: priority = 'cost'
    elif 'performance' in user_message: priority = 'performance'
    if not service_type: return "I can help, but please mention if you need 'compute', 'storage', or 'database' services."
    if not usage: return "Please specify your expected usage (e.g., '100 hours' or '50 GB')."
    if not budget: return "It's helpful if you can provide a monthly budget in Rupees."
    results = get_simple_recommendation(service_type, usage, budget, priority)
    if "error" in results: return results["error"]
    best = results["recommendations"][0]
    response = (f"Based on your request, the best option is **{best['provider']} - {best['service']}**.\n"
                f"Estimated Cost: **₹{best['total_cost']:,.0f}/month** | Performance: **{best['performance']}/10**.")
    return response