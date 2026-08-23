from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import DoctorProfile, Appointment, PreVisitSummary, PostVisitSummary, User
from app.services.llm_service import generate_post_visit_summary
from app import db
import datetime

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

@doctor_bp.route('/dashboard')
@login_required
def dashboard():
    # Ensure only doctors can access this
    if current_user.role != 'doctor':
        flash('Access denied.', 'error')
        return redirect(url_for('auth.login'))

    # Get the doctor's profile ID
    doctor = DoctorProfile.query.filter_by(user_id=current_user.id).first()
    
    # Fetch all confirmed appointments for this doctor, ordered by time
    appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.status == 'confirmed'
    ).order_by(Appointment.start_time).all()
    
    # We need to manually zip the pre-visit summaries with the appointments 
    # since we didn't set up a direct SQLAlchemy relationship for them yet
    appointments_data = []
    for appt in appointments:
        patient = User.query.get(appt.patient_id)
        pre_summary = PreVisitSummary.query.filter_by(appointment_id=appt.id).first()
        appointments_data.append({
            'appointment': appt,
            'patient': patient,
            'pre_summary': pre_summary
        })

    return render_template('doctor_dashboard.html', appointments_data=appointments_data)