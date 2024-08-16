from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('base.html')

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
    print(f"Calling API: {API_URL} with data: {data}")  # Log the API call details
    response = requests.post(API_URL, json=data, headers=headers)
    print(f"API Response Status: {response.status_code}")  # Log the response status code
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
        'userInput': f"the last question was: {last_question} | user input: {user_input}"
    }
    print(f"Calling API: {API_URL} with data: {data}")  # Log the API call details
    response = requests.post(API_URL, json=data, headers=headers)
    print(f"API Response Status: {response.status_code}")  # Log the response status code
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
            
            # Update last_question to the current question before moving forward
            old_question = last_question
            return render_template('practice.html', old_question=old_question, feedback=feedback, correct=correct, question=new_question)
        else:
            return render_template('practice.html', error="Failed to submit answer. Please try again.")
    else:
        question = get_next_question()
        if question:
            return render_template('practice.html', question=question.get('newQuestion'))
        else:
            return render_template('practice.html', error="Failed to load question. Please try again.")
