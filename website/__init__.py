from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

# Initialize the extensions
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Initialize the extensions with the app
    db.init_app(app)
    mail.init_app(app)  # Initialize Flask-Mail extension

    # Register blueprints
    from .models import User
    from .views import views
    from .auth import auth  # Import the auth blueprint

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')  # Register the auth blueprint

    # Set up login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Update to use auth.login since the login route is in auth.py
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create database tables
    with app.app_context():
        db.create_all()

    return app