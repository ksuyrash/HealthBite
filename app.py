from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager  # Import LoginManager
import os
from dotenv import load_dotenv
from database import create_database, db  # Import create_database and db

migrate = Migrate()
login_manager = LoginManager()  # Initialize LoginManager

def create_app():
    app = Flask(__name__, template_folder="website/templates")  # Explicitly set template folder
    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print("DATABASE_URL:", os.getenv("DATABASE_URL"))
    db.init_app(app)  # Ensure db is initialized with the app
    print("Debug: db.init_app called successfully")  # Debugging line
    migrate.init_app(app, db)

    login_manager.init_app(app)  # Attach LoginManager to the app
    login_manager.login_view = 'auth.login'  # Set the login view

    from website.views import views
    from website.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')  # Ensure this line exists

    from website.models import User

    @login_manager.user_loader
    def load_user(user_id):
        print(f"Debug: Loading user with ID {user_id}")  # Debugging line
        with current_app.app_context():  # Use current_app to ensure the app context is active
            return User.query.get(int(user_id))  # Define user loader callback

    with app.app_context():  # Ensure app context is active during database creation
        create_database(app)  # Call create_database

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)