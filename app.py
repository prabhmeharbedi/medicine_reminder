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
app.config['MAIL_USERNAME'] = 'xabc12962@gmail.com'  # Replace with your Gmail
app.config['MAIL_PASSWORD'] = 'lxsytxfknuixgxlk'     # Replace with your App Password

db.init_app(app)
mail = Mail(app)

# Models
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    medicine_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean, default=False)

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
        reminder_time=datetime.strptime(data['reminder_time'], "%Y-%m-%dT%H:%M")
    )
    db.session.add(new_reminder)
    db.session.commit()
    print(f"Reminder added for {data['email']} at {data['reminder_time']}")
    return jsonify({"message": "Reminder added successfully!"}), 201

# Email Function
def send_email(to, subject, body):
    print(f"Preparing to send email to {to}")
    try:
        with app.app_context():
            msg = Message(
                subject=subject,
                recipients=[to],
                body=body,
                sender=app.config['MAIL_USERNAME']
            )
            mail.send(msg)
            print(f"Email sent successfully to {to}")
    except Exception as e:
        print(f"Error sending email to {to}: {str(e)}")

# Scheduler Job
def check_and_send_reminders():
    print("Checking for reminders...")
    with app.app_context():
        now = datetime.now()
        reminders = Reminder.query.filter(Reminder.reminder_time <= now, Reminder.sent == False).all()
        print(f"Reminders found: {len(reminders)}")
        for reminder in reminders:
            try:
                body = f"Time to take your medicine: {reminder.medicine_name} ({reminder.dosage})"
                send_email(reminder.email, "Medicine Reminder", body)
                reminder.sent = True
                db.session.commit()
                print(f"Email sent and marked as sent for {reminder.email}")
            except Exception as e:
                print(f"Failed to send email: {str(e)}")

# Initialize and Start Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_and_send_reminders, 'interval', minutes=1)  # Checks every 1 minute
scheduler.start()
print("Scheduler started...")

# Database initialization and app launch
if __name__ == "__main__":
    print(f"Database path: {os.path.abspath('reminders.db')}")
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=False, host='0.0.0.0', port=8000)