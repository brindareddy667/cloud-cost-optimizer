# next_month_prediction.py
import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_next_month_cost():
    """
    Reads past usage data, predicts next month's cost, and returns the data.
    """
    try:
        data = pd.read_csv('usage_data.csv')
        
        X = data[['Usage_Hours']]
        y = data['Cost']

        model = LinearRegression()
        model.fit(X, y)

        # Predict for next month (example: +30 hours usage for a noticeable change)
        next_month_usage = data['Usage_Hours'].iloc[-1] + 30
        prediction = model.predict([[next_month_usage]])[0]

        # Prepare data to send to the frontend
        past_costs = y.tolist()
        predicted_cost = prediction

        return {
            'past_costs': past_costs,
            'predicted_cost': predicted_cost
        }

    except FileNotFoundError:
        # Return default data if the file is missing
        return {
            'past_costs': [0, 0, 0, 0, 0, 0],
            'predicted_cost': 0,
            'error': 'usage_data.csv not found.'
        }