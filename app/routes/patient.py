from flask import Blueprint
from flask_login import login_required, current_user

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

@patient_bp.route('/dashboard')
@login_required
def dashboard():
    return f"<h1>Welcome to your Dashboard, {current_user.name}!</h1> <a href='/logout'>Logout</a>"