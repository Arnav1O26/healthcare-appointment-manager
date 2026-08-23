from app import db
from app.models import Appointment
from datetime import datetime, timedelta

def hold_slot(patient_id, doctor_id, start_time_str, duration_mins=30):
    """
    Attempts to place a temporary hold on a specific time slot.
    Uses database row-locking to prevent double-booking.
    """
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
    end_time = start_time + timedelta(minutes=duration_mins)

    try:
        # 1. Query for any existing appointment at this exact time that is NOT cancelled.
        # .with_for_update() locks these rows in the database until this transaction finishes.
        existing_appt = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.start_time == start_time,
            Appointment.status.in_(['held', 'pending', 'confirmed'])
        ).with_for_update().first()

        # 2. If it exists, someone else beat us to it.
        if existing_appt:
            return {"success": False, "message": "This slot was just taken by someone else."}

        # 3. If it's free, create the temporary hold
        new_appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            start_time=start_time,
            end_time=end_time,
            status='held'
        )
        
        db.session.add(new_appointment)
        db.session.commit() # The lock is released here
        
        return {
            "success": True, 
            "appointment_id": new_appointment.id, 
            "message": "Slot held! Please fill out your symptoms within 10 minutes."
        }

    except Exception as e:
        db.session.rollback() # Undo everything if an error occurs
        return {"success": False, "message": str(e)}