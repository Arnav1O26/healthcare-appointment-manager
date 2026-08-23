from flask import Blueprint, render_template
from flask_login import login_required, current_user

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

@patient_bp.route('/dashboard')
@login_required
def dashboard():
    # Later, we will load actual appointments from the database here
    return render_template('patient_dashboard.html', user=current_user)