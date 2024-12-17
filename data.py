from app import db, app  # Import both db and the Flask app

with app.app_context():  # Push the app context
    db.create_all()
    print("Database initialized!")