from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests

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

@app.route('/directory')
def directory():
    return render_template('directory.html', employees=employees)

@app.route('/news')
def news_page():
    return render_template('news.html', news=news)

@app.route('/documents')
def documents_page():
    return render_template('documents.html', documents=documents)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html', events=events)

# New API endpoint to handle requests to an external API
@app.route('/api/employee_assistant', methods=['POST'])
def employee_assistant():
    # External API URL
    external_api_url = "https://demo.airia.com/platform/api/PipelineExecution/employee_assistant"
    
    # Headers (including authorization token if required)
    headers = {
        "X-API-Key": "d465b2d3-4b4c-4167-83ee-e7c144664b35",
        "Content-Type": "application/json"
    }

    try:
        # Make a request to the external API
        response = requests.get(external_api_url, headers=headers)

        # Check if the response was successful
        if response.status_code == 200:
            # Return the API response to the frontend
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch data from external API", "status_code": response.status_code}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
