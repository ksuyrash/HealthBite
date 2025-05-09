from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from website import create_app, db
from website.auth import mail

migrate = Migrate()
login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder="website/templates")

    # Main settings
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
    app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL") == "True"
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

    print("DATABASE_URL:", os.getenv("DATABASE_URL"))
    db.init_app(app)
    print("Debug: db.init_app called successfully")
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login for protected routes
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'error'

    # Custom login check to exempt /sign-up
    @login_manager.request_loader
    def load_user_from_request(request):
        if request.path == '/sign-up':
            return None  # Allow access to sign-up without login
        user_id = request.cookies.get('user_id')
        if user_id:
            return User.query.get(int(user_id))
        return None

    mail.init_app(app)

    from website.views import views
    from website.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from website.models import User

    @login_manager.user_loader
    def load_user(user_id):
        print(f"Debug: Loading user with ID {user_id}")
        with current_app.app_context():
            return User.query.get(int(user_id))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)