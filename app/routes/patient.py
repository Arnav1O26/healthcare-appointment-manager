from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from app import db
from app.models import DoctorProfile, User, Appointment, PreVisitSummary, PostVisitSummary, DoctorLeave
from app.services.slot_service import get_available_slots
from app.services.booking_service import hold_slot
from app.services.llm_service import generate_pre_visit_summary

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

@patient_bp.route('/dashboard')
@login_required
def dashboard():
    # Later, we will load actual appointments from the database here
    return render_template('patient_dashboard.html', user=current_user)

@patient_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    # Fetch all unique specializations to populate the filter dropdown
    all_specs = db.session.query(DoctorProfile.specialization).distinct().all()
    specializations = [spec[0] for spec in all_specs] # Flatten the list
    
    # Check if the user applied a filter via the URL (e.g., ?specialization=Cardiologist)
    selected_spec = request.args.get('specialization')

    # 1. Get a list of doctors, applying the filter if one exists
    if selected_spec:
        doctors = DoctorProfile.query.join(User).filter(DoctorProfile.specialization == selected_spec).all()
    else:
        doctors = DoctorProfile.query.join(User).all()
    
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        symptoms = request.form.get('symptoms')

        # Combine date and time for the database
        start_time_str = f"{date_str} {time_str}"
        
        # 2. Attempt to lock the slot using our concurrency service
        hold_result = hold_slot(current_user.id, doctor_id, start_time_str)
        
        if not hold_result['success']:
            flash(hold_result['message'], 'error')
            return redirect(url_for('patient.book_appointment'))
            
        appointment_id = hold_result['appointment_id']

        # 3. Process Symptoms with AI (Pre-visit Summary)
        ai_result = generate_pre_visit_summary(symptoms)
        
        # Save the AI summary (or the raw text if AI failed) to the database
        summary_record = PreVisitSummary(
            appointment_id=appointment_id,
            raw_symptoms=symptoms,
            ai_summary=ai_result['summary'] if ai_result['success'] else None
        )
        db.session.add(summary_record)
        
        # 4. Confirm the appointment (changing status from 'held' to 'confirmed')
        appointment = Appointment.query.get(appointment_id)
        appointment.status = 'confirmed'
        db.session.commit()
        
        # Send confirmation email to the patient
        # (Assuming you imported send_email at the top of patient.py)
        # subject = "Appointment Confirmed"
        # body = f"Your appointment is confirmed for {start_time_str}."
        # send_email(current_user.email, subject, body)
        
        flash('Appointment booked successfully! The doctor will review your symptoms.', 'success')
        return redirect(url_for('patient.dashboard'))

    # Pass the specializations and the currently selected spec to the template
    return render_template('book_appointment.html', 
                           doctors=doctors, 
                           specializations=specializations, 
                           selected_spec=selected_spec)

# API Route to get time slots dynamically when the user picks a date via JavaScript
@patient_bp.route('/api/slots')
@login_required
def get_slots():
    doctor_id = request.args.get('doctor_id')
    date_str = request.args.get('date')

    if not doctor_id or not date_str:
        return {"slots": []}

    # 1. Convert the string date into a proper Python date object
    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # 2. Check if the doctor is on leave
    is_on_leave = DoctorLeave.query.filter_by(doctor_id=doctor_id, leave_date=target_date).first()
    if is_on_leave:
        return {"slots": []} # Return empty slots if on leave

    # 3. Fetch standard slots if not on leave
    result = get_available_slots(doctor_id, date_str)
    return {"slots": result.get('slots', [])}

@patient_bp.route('/history')
@login_required
def history():
    # Fetch all appointments for the logged-in patient
    appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.start_time.desc()).all()
    
    history_data = []
    for appt in appointments:
        doc_profile = DoctorProfile.query.get(appt.doctor_id)
        doctor_user = User.query.get(doc_profile.user_id) if doc_profile else None
        post_summary = PostVisitSummary.query.filter_by(appointment_id=appt.id).first()
        
        history_data.append({
            'appointment': appt,
            'doctor_name': doctor_user.name if doctor_user else 'Unknown',
            'specialization': doc_profile.specialization if doc_profile else 'General',
            'post_summary': post_summary
        })

    return render_template('patient_history.html', history_data=history_data)