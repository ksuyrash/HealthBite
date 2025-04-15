# filepath: c:\Users\Xu\Documents\HealthBite\HealthBite\website\config.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.")

# Email configuration for Flask-Mail
MAIL_SERVER = os.getenv("MAIL_SERVER")
if not MAIL_SERVER:
    raise ValueError("MAIL_SERVER environment variable is not set.")

MAIL_PORT = os.getenv("MAIL_PORT", 587)  # Default to 587 if not set
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"  # Default to True
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"  # Default to False
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
if not MAIL_USERNAME:
    raise ValueError("MAIL_USERNAME environment variable is not set.")

MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
if not MAIL_PASSWORD:
    raise ValueError("MAIL_PASSWORD environment variable is not set.")

MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)  # Use username as default sender