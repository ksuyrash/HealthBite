from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app as app
from website.models import User
from werkzeug.security import generate_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from website import mail  # <-- This pulls in the mail instance from __init__.py

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found. Please check your email.', category='error')
            return render_template('login.html', user=current_user)

        if user and not user.check_password(password):
            flash('Incorrect password. Please try again.', category='error')
            return render_template('login.html', user=current_user)

        login_user(user, remember=True)
        flash('Logged in successfully!', category='success')
        next_page = request.args.get('next')
        return redirect(next_page or url_for('views.home'))

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
        height = request.form.get('height')
        weight = request.form.get('weight')
        age = request.form.get('age')
        gender = request.form.get('gender')

        if not email or not first_name or not password1 or not password2:
            flash('All fields are required.', category='error')
            return render_template('sign_up.html', user=current_user)

        if password1 != password2:
            flash('Passwords do not match.', category='error')
            return render_template('sign_up.html', user=current_user)

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
            flash(f"An error occurred: {str(e)}", category='error')

    return render_template('sign_up.html', user=current_user)

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate token
            token = URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps(email, salt='password-reset')
            reset_url = url_for('auth.reset_password_token', token=token, _external=True)

            # Compose email
            msg = Message('Password Reset Request', recipients=[email])
            msg.body = f'Hello,\n\nClick the link below to reset your password:\n{reset_url}\n\nIf you did not request this, you can safely ignore this email.\n\n- HealthBite Team'

            # Debug SMTP config
            print("📬 Attempting to send email with config:")
            print("MAIL_SERVER:", app.config.get("MAIL_SERVER"))
            print("MAIL_PORT:", app.config.get("MAIL_PORT"))
            print("MAIL_USERNAME:", app.config.get("MAIL_USERNAME"))
            print("MAIL_PASSWORD:", (app.config.get("MAIL_PASSWORD") or "")[:3] + "*****")
            print("MAIL_USE_TLS:", app.config.get("MAIL_USE_TLS"))
            print("MAIL_USE_SSL:", app.config.get("MAIL_USE_SSL"))

            try:
                mail.send(msg)
                flash(f'Password reset link sent to {email}.', category='info')
            except Exception as e:
                flash(f'Error sending email: {str(e)}', category='error')
        else:
            flash('Email not registered.', category='error')
    return render_template('reset_password.html', user=current_user)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    try:
        email = URLSafeTimedSerializer(app.config['SECRET_KEY']).loads(token, salt='password-reset', max_age=3600)
    except SignatureExpired:
        flash('The reset link has expired.', category='error')
        return redirect(url_for('auth.reset_password'))

    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash('Passwords do not match.', category='error')
            return render_template('reset_password_token.html', token=token)

        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(password1, method='pbkdf2:sha256')
        db.session.commit()
        flash('Password updated successfully!', category='success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password_token.html', token=token)




