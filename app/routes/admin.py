from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, DoctorProfile, Appointment
from app import db

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