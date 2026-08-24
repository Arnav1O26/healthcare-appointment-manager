from markdown import markdown
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

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.patient import patient_bp
    from app.routes.doctor import doctor_bp
    from app.routes.calendar import calendar_bp
    
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp) 
    app.register_blueprint(calendar_bp)
    
    # User loader for Flask-Login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Add Markdown filter for the Jinja templates
    @app.template_filter('markdown')
    def render_markdown(text):
        if text:
            return markdown(text)
        return ""
    
    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    return app