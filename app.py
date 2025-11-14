from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

from cost_prediction import calculate_cost_from_params
from next_month_prediction import predict_next_month_cost
from cost_optimizer import get_simple_optimizations
import bot_logic

# Tells Flask to look for HTML files in the current directory
app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

# --- Part 1: Specific Routes for Each HTML Page ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prediction.html')
def prediction_page():
    return render_template('prediction.html')
    
@app.route('/prediction-result.html')
def prediction_result_page():
    return render_template('prediction-result.html')

@app.route('/optimization.html')
def optimization_page():
    return render_template('optimization.html')

@app.route('/bot.html')
def bot_page():
    return render_template('bot.html')

@app.route('/calculator.html')
def calculator_page():
    return render_template('calculator.html')

@app.route('/chat-bot.html')
def chatbot_page():
    return render_template('chat-bot.html')


# --- Part 2: API Endpoints (RESTORED) ---
@app.route('/api/calculate', methods=['POST'])
def handle_calculation():
    data = request.json
    final_cost = calculate_cost_from_params(data.get('vm_count', 0), data.get('instance_type', ''), data.get('usage_hours', 0), data.get('currency', 'USD'))
    return jsonify({'cost': final_cost})

@app.route('/api/predict', methods=['GET'])
def handle_prediction():
    prediction_data = predict_next_month_cost()
    return jsonify(prediction_data)

@app.route('/api/optimize', methods=['GET'])
def handle_optimization():
    recommendation_data = get_simple_optimizations()
    return jsonify(recommendation_data)

@app.route('/api/simple-bot', methods=['POST'])
def handle_simple_bot():
    data = request.json
    result = bot_logic.get_simple_recommendation(data.get('service_type'), data.get('usage'), data.get('budget'), data.get('priority'))
    return jsonify(result)

@app.route('/api/pro-bot', methods=['POST'])
def handle_pro_bot():
    data = request.json
    response_message = bot_logic.get_architecture_recommendation(data.get('message'))
    return jsonify({'reply': response_message})

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    data = request.json
    response_message = bot_logic.get_chat_response(data.get('message'))
    return jsonify({'reply': response_message})


# --- Part 3: Catch-All Route for Other Files (CSS, PNG, etc.) ---
@app.route('/<path:filename>')
def serve_other_files(filename):
    return send_from_directory('.', filename)


if __name__ == '__main__':
    app.run(debug=True)
