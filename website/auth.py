from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app as app
from website.models import User
from werkzeug.security import generate_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from website import mail

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
            height=height,
            weight=weight,
            age=age,
            gender=gender
        )
        new_user.set_password(password1)

        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account has been created!', category='success')
            return redirect(url_for('views.home'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", category='error')     # test change


    return render_template('sign_up.html', user=current_user)

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps(email, salt='password-reset')
            reset_url = url_for('auth.reset_password_token', token=token, _external=True)

            msg = Message('Password Reset Request', recipients=[email])
            msg.body = f'Hello,\n\nClick the link below to reset your password:\n{reset_url}\n\nIf you did not request this, you can safely ignore this email.\n\n- HealthBite Team'

            try:
                mail.send(msg)
                flash(f'Password reset link sent to {email}.', category='info')
            except Exception as e:
                flash(f"Error sending email: {str(e)}", category='error')
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
        if user:
            app.logger.info(f"[RESET] Resetting password for user: {email}")
            app.logger.info(f"[RESET] Old password hash: {user.password}")
            user.set_password(password1)
            app.logger.info(f"[RESET] New password hash: {user.password}")
            try:
                db.session.commit()
                app.logger.info("[RESET] Password committed to DB successfully.")
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"[RESET] Error during commit: {str(e)}")
                flash("Database error occurred during password reset.", category='error')
                return redirect(url_for('auth.reset_password'))

            return redirect(url_for('auth.password_reset_success'))
        else:
            flash('User not found.', category='error')
            return redirect(url_for('auth.reset_password'))

    return render_template('reset_password_token.html', token=token)

@auth.route('/password-reset-success')
def password_reset_success():
    return render_template('password_reset_success.html')






