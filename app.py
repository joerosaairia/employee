from flask import Flask, render_template
from flask_cors import CORS

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

if __name__ == '__main__':
    app.run(debug=True)
