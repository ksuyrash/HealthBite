from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()  # Ensure this is the single instance used everywhere

def create_database(app):
    with app.app_context():  # Ensure app context is active
        if not os.path.exists('instance'):
            os.makedirs('instance')  # Create instance folder if it doesn't exist
        db.create_all()  # Create all tables
        print("Debug: Database created successfully")  # Debugging line