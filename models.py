from extensions import db

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    medicine_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean, default=False)