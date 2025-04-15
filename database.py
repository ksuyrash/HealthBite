from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Main database instance

def create_database(app):
    with app.app_context():
        db.create_all()
        print("✅ Tables created successfully in the remote MySQL database.")
