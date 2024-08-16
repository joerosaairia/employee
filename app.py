from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Dummy data
employees = [
    {"name": "Alice Johnson", "position": "Software Engineer", "email": "alice@example.com"},
    {"name": "Bob Smith", "position": "Project Manager", "email": "bob@example.com"},
    {"name": "Carol White", "position": "HR Specialist", "email": "carol@example.com"}
]

news = [
    {"title": "Company Q2 Results", "content": "We have exceeded our targets for Q2..."},
    {"title": "New Office Opening", "content": "Our new office in San Francisco is now open..."}
]

documents = [
    {"title": "Employee Handbook", "link": "#"},
    {"title": "HR Policies", "link": "#"}
]

events = [
    {"date": "2024-08-10", "event": "Company Picnic"},
    {"date": "2024-09-15", "event": "Annual General Meeting"}
]

@app.route('/')
def home():
    return render_template('home.html')


API_URL = 'https://demo.airia.com/platform/api/PipelineExecution/education'
API_KEY = 'd465b2d3-4b4c-4167-83ee-e7c144664b35'  # Your actual API key

def get_next_question():
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
    }
    data = {
        'userInput': 'get a new question'
    }
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json().get('result')
        if isinstance(result, str):
            result = json.loads(result)
        return result
    else:
        return None

def submit_answer(last_question, user_input):
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
    }
    data = {
        'userInput': f"last question: {last_question} | user input: {user_input}"
    }
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json().get('result')
        if isinstance(result, str):
            result = json.loads(result)
        return result
    else:
        return None

@app.route('/practice', methods=['GET', 'POST'])
def practice():
    if request.method == 'POST':
        last_question = request.form.get('last_question')
        user_input = request.form.get('user_input')
        feedback_response = submit_answer(last_question, user_input)
        
        if feedback_response:
            feedback = feedback_response.get('feedback')
            correct = feedback_response.get('correct')
            new_question = feedback_response.get('newQuestion')
            
            return render_template('practice.html', old_question=last_question, feedback=feedback, correct=correct, question=new_question)
        else:
            return render_template('practice.html', error="Failed to submit answer. Please try again.")
    else:
        question = get_next_question()
        if question:
            return render_template('practice.html', question=question.get('newQuestion'))
        else:
            return render_template('practice.html', error="Failed to load question. Please try again.")

# API route to handle chatbot requests
@app.route('/api/employee_assistant', methods=['POST'])
def employee_assistant():
    external_api_url = "https://demo.airia.com/platform/api/PipelineExecution/joe_test_pipeline_2"
    
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