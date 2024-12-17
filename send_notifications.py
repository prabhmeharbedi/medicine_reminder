from app import app, db, mail
from flask_mail import Message
from models import Reminder
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

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

def check_and_send_reminders():
    print("Checking for reminders...")
    with app.app_context():
        now = datetime.now()
        print(f"Current time: {now}")  # Log current time
        reminders = Reminder.query.all()
        for reminder in reminders:
            print(f"Stored reminder time: {reminder.reminder_time}, Sent: {reminder.sent}")
        
        # Filter logic
        reminders_to_send = Reminder.query.filter(Reminder.reminder_time <= now, Reminder.sent == False).all()
        print(f"Reminders found: {len(reminders_to_send)}")
        
        for reminder in reminders_to_send:
            body = f"Time to take your medicine: {reminder.medicine_name} ({reminder.dosage})"
            send_email(reminder.email, "Medicine Reminder", body)
            reminder.sent = True
            db.session.commit()
            print(f"Reminder marked as sent for: {reminder.email}")

scheduler = BackgroundScheduler()
scheduler.add_job(check_and_send_reminders, 'interval', seconds=10)  # Runs every 10 seconds
scheduler.start()

print("Scheduler started. Monitoring reminders...")
while True:
    pass  # Keeps the script running