from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, DoctorProfile, Appointment
from app import db
from datetime import datetime
from app.models import DoctorLeave
from app.services.email_service import send_email

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('auth.login'))
        
    total_patients = User.query.filter_by(role='patient').count()
    total_doctors = User.query.filter_by(role='doctor').count()
    total_appointments = Appointment.query.count()
    doctors = DoctorProfile.query.all()
    
    return render_template('admin_dashboard.html', 
                           total_patients=total_patients,
                           total_doctors=total_doctors,
                           total_appointments=total_appointments,
                           doctors=doctors)

@admin_bp.route('/add_doctor', methods=['POST'])
@login_required
def add_doctor():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
        
    email = request.form.get('email')
    if User.query.filter_by(email=email).first():
        flash('Email already registered.', 'error')
        return redirect(url_for('admin.dashboard'))
        
    # Create User
    new_user = User(name=request.form.get('name'), email=email, role='doctor')
    new_user.set_password(request.form.get('password'))
    db.session.add(new_user)
    db.session.commit() 
    
    # Create Profile
    new_profile = DoctorProfile(
        user_id=new_user.id,
        specialization=request.form.get('specialization'),
        working_hours_start='09:00',
        working_hours_end='17:00',
        slot_duration_mins=30
    )
    db.session.add(new_profile)
    db.session.commit()
    
    flash('Doctor added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/add_leave', methods=['POST'])
@login_required
def add_leave():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
        
    doctor_id = request.form.get('doctor_id')
    leave_date_str = request.form.get('leave_date')
    leave_date = datetime.strptime(leave_date_str, '%Y-%m-%d').date()
    
    # 1. Mark the leave in the database
    new_leave = DoctorLeave(doctor_id=doctor_id, leave_date=leave_date)
    db.session.add(new_leave)
    
    # 2. Find and cancel conflicting appointments
    conflicts = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        db.func.date(Appointment.start_time) == leave_date,
        Appointment.status == 'confirmed'
    ).all()
    
    for appt in conflicts:
        appt.status = 'cancelled'
        patient = User.query.get(appt.patient_id)
        
        # Send cancellation email to the patient
        subject = "Appointment Cancellation Notice"
        body = f"Dear {patient.name},\n\nUnfortunately, your appointment on {appt.start_time.strftime('%b %d, %Y at %I:%M %p')} has been cancelled because the doctor is unavailable. Please log in to your dashboard to reschedule.\n\nThank you,\nClinic Admin"
        
        send_email(patient.email, subject, body)
        
    db.session.commit()
    flash(f'Leave added. {len(conflicts)} appointments were automatically cancelled.', 'success')
    return redirect(url_for('admin.dashboard'))