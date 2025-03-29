from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()  # Ensure this is the single instance used everywhere

def create_database(app):
    if not os.path.exists('healthbite.db'):  # Replace with your database file path if using SQLite
        with app.app_context():
            db.create_all()
            print("Database created successfully!")