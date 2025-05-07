from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@views.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        height = request.form.get('height')
        weight = request.form.get('weight')
        age = request.form.get('age')
        gender = request.form.get('gender')

        # Check for missing fields
        if not all([email, first_name, password1, password2, height, weight, age, gender]):
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('views.sign_up'))

        # Validate email format
        if '@' not in email or '.' not in email:
            flash('Invalid email format. Please use an email like example@domain.com.', 'error')
            return redirect(url_for('views.sign_up'))

        # Validate password match
        if password1 != password2:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('views.sign_up'))

        # Validate password length
        if len(password1) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return redirect(url_for('views.sign_up'))

        # Validate numeric fields
        try:
            height = float(height)
            weight = float(weight)
            age = int(age)
            if height <= 0 or weight <= 0 or age <= 0:
                flash('Height, weight, and age must be positive numbers.', 'error')
                return redirect(url_for('views.sign_up'))
        except ValueError:
            flash('Height, weight, and age must be valid numbers.', 'error')
            return redirect(url_for('views.sign_up'))

        # Check for existing user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This email is already registered. Please use a different email or log in.', 'error')
            return redirect(url_for('views.sign_up'))

        # Create new user
        new_user = User(
            email=email,
            first_name=first_name,
            height=height,
            weight=weight,
            age=age,
            gender=gender
        )
        new_user.set_password(password1)

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)  # Log in the user after sign-up
        return redirect(url_for('views.home'))  # Redirect to homepage

    return render_template('sign_up.html', user=current_user)