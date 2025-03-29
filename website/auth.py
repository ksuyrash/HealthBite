from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):  # Use check_password method
            login_user(user)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Login failed. Check your email and password.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    print("Debug: sign_up route called")  # Debugging line
    if request.method == 'POST':
        # Debugging: Print the entire request.form object
        print(f"Debug: request.form={request.form}")

        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        height = request.form.get('height') or 0  # Default to 0 if empty
        weight = request.form.get('weight') or 0  # Default to 0 if empty
        age = request.form.get('age') or 0  # Default to 0 if empty
        gender = request.form.get('gender') or "Unknown"  # Default to "Unknown" if empty

        # Debugging: Print retrieved form data
        print(f"Debug: email={email}, first_name={first_name}, password1={password1}, password2={password2}")
        print(f"Debug: height={height}, weight={weight}, age={age}, gender={gender}")

        # Fallback for missing data
        if not email or not first_name or not password1 or not password2:
            flash('All fields are required.', category='error')
            return render_template('sign_up.html', user=current_user)

        # Validate passwords
        if password1 != password2:
            flash('Passwords do not match.', category='error')
            return render_template('sign_up.html', user=current_user)

        # Convert and validate numeric fields
        try:
            height = float(height) if height else None  # Convert height to float
            weight = float(weight) if weight else None  # Convert weight to float
            age = int(age) if age else None  # Convert age to integer
        except ValueError:
            flash('Height, weight, and age must be valid numbers.', category='error')
            return render_template('sign_up.html', user=current_user)

        # Create a new user with the new fields
        new_user = User(
            email=email,
            first_name=first_name,
            password=generate_password_hash(password1, method='pbkdf2:sha256'),
            height=height,
            weight=weight,
            age=age,
            gender=gender
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account has been created!', category='success')
            return redirect(url_for('views.home'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", category="error")

    return render_template('sign_up.html', user=current_user)
