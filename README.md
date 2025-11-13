# ☁️ Smart Cloud Cost Manager

**Smart Cloud Cost Manager** is a comprehensive web application designed to help users efficiently forecast, manage, and optimize their cloud expenditures in real-time. It addresses the complexity of cloud billing by providing tools for cost prediction, automated optimization, and an AI-powered service selector.

## 🚀 Features

The application consists of three core modules:

### 1. Prediction Suite 📊
* **Cost Calculator:** Estimates monthly costs for new resources based on user inputs (VM count, instance type, region, usage hours).
* **Next-Month Forecast:** Uses **Linear Regression** on historical usage data (`usage_data.csv`) to predict upcoming bills.

### 2. Optimization Engine ⚙️
* **Rightsizing Advice:** Identifies underutilized resources (e.g., CPU usage < 20%) and suggests downsizing.
* **Shutdown Scheduling:** Detects instances running 24/7 and suggests shutdown schedules for off-hours savings
* **Visuals:** Provides "Current vs. Optimized" cost comparison graphs.

### 3. Cloud Bot (Agentblazer) 🤖
* **Simple Mode:** Form-based chat for basic queries.
* [**Pro Mode (Architecture Advisor):** Uses keyword matching to recommend specific compute, database, or storage services based on project descriptions.
* **Live Chat:** Conversational interface for detailed analysis.

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript.
* **Backend:** Python, Flask.
* **Machine Learning:** Scikit-learn (Linear Regression), Pandas for data handling.
* **Data:** Mock datasets simulating real-world cloud usage (`usage_data.csv`, `instance_pricing.csv`).

## 📂 Project Structure

```bash
├── app.py                 # Main Flask application
├── cost_prediction.py     # Logic for cost calculation
├── next_month_prediction.py # ML model for forecasting
├── cost_optimizer.py      # Rule-based optimization engine
├── bot_logic.py           # Logic for the Cloud Bot
├── templates/             # HTML files
├── static/                # CSS and JS files
└── data/                  # CSV datasets
