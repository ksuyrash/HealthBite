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
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('An account with this email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters long.', category='error')
        elif len(first_name) < 2:
            flash('First name must be at least 2 characters long.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters long.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password_hash=generate_password_hash(password1, method='pbkdf2:sha256')  # ✅ Correct field name
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
