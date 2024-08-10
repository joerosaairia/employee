from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/employee_assistant', methods=['POST'])
@app.route('/api/employee_assistant', methods=['POST'])
def employee_assistant():
    print("Employee Assistant API Called")  # Debugging statement
    external_api_url = "https://demo.airia.com/platform/api/PipelineExecution/get_bitcoin_price"
    headers = {
        "X-API-Key": "d465b2d3-4b4c-4167-83ee-e7c144664b35",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(external_api_url, headers=headers, json=request.json)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            error_message = response.json().get('message', 'Unknown error occurred')
            return jsonify({"error": error_message, "status_code": response.status_code}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
