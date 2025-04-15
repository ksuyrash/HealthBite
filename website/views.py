from flask import Blueprint, render_template, request, redirect, url_for, current_app  # Added current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash  # Ensure this import stays
from database import db  # Ensure this is the same db instance used everywhere
from website.models import User  # Use absolute import

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['firstName']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            return "Passwords do not match", 400

        user = User.query.filter_by(email=email).first()  # Query using the consistent db instance
        if user:
            return "User already exists", 400

        new_user = User(
            email=email,
            first_name=first_name,
            password=generate_password_hash(password1, method='pbkdf2:sha256')  # Use a valid hash method
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
