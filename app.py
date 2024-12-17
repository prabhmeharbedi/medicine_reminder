from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from extensions import db
import os

# Initialize Flask app
app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reminders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'xabc12962@gmail.com'
app.config['MAIL_PASSWORD'] = 'lxsytxfknuixgxlk'

db.init_app(app)
mail = Mail(app)

# Models
from models import Reminder

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    data = request.json
    new_reminder = Reminder(
        email=data['email'],
        medicine_name=data['medicine_name'],
        dosage=data['dosage'],
        reminder_time=datetime.strptime(data['reminder_time'], "%Y-%m-%dT%H:%M")  # Fix format
    )
    db.session.add(new_reminder)
    db.session.commit()
    return jsonify({"message": "Reminder added successfully!"}), 201

# Database initialization
if __name__ == "__main__":
    print(f"Database path: {os.path.abspath('reminders.db')}")
    with app.app_context():
        db.create_all()
    app.run(debug=True)