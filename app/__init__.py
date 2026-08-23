from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # We will build this route later

def create_app():
    app = Flask(__name__)
    
    # Configure app using environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key-for-dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///healthcare.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind extensions to the app
    db.init_app(app)
    login_manager.init_app(app)

    # We will register our blueprints (routes) here later
    
    return app