from flask_login import UserMixin
from sqlalchemy.sql import func
from database import db
from datetime import datetime  # Ensure this import stays
from werkzeug.security import generate_password_hash, check_password_hash  # Ensure this import stays

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Explicitly define the table name
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)  # Use the existing 'password' column
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Use datetime.utcnow
    edited_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    height = db.Column(db.Float, nullable=True)  # Height in cm
    weight = db.Column(db.Float, nullable=True)  # Weight in kg
    age = db.Column(db.Integer, nullable=True)  # Age in years
    gender = db.Column(db.String(50), nullable=True)  # Gender

    def set_password(self, password):
        self.password = generate_password_hash(password)  # Store hashed password in 'password' column

    def check_password(self, password):
        return check_password_hash(self.password, password)  # Verify against 'password' column


