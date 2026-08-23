from datetime import datetime, timedelta
from app.models import DoctorProfile, DoctorLeave, Appointment
from app import db

def get_available_slots(doctor_id, date_str):
    """
    Calculates available time slots for a given doctor and date.
    date_str should be in 'YYYY-MM-DD' format.
    """
    doctor = DoctorProfile.query.filter_by(id=doctor_id).first()
    if not doctor:
        return {"error": "Doctor not found"}

    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # 1. Check if the doctor is on leave
    leave = DoctorLeave.query.filter_by(doctor_id=doctor_id, leave_date=target_date).first()
    if leave:
        return {"date": date_str, "slots": [], "message": "Doctor is on leave"}

    # 2. Define the start and end of the working day
    start_time = datetime.strptime(f"{date_str} {doctor.working_hours_start}", '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(f"{date_str} {doctor.working_hours_end}", '%Y-%m-%d %H:%M')
    slot_duration = timedelta(minutes=doctor.slot_duration_mins)

    # 3. Fetch already booked appointments for this date
    # We only look at appointments that are NOT cancelled
    appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.status != 'cancelled'
    ).all()
    
    # Extract just the start times of booked appointments that fall on our target date
    booked_times = [
        app.start_time for app in appointments 
        if app.start_time.date() == target_date
    ]

    # 4. Generate all possible slots and filter out the booked ones
    available_slots = []
    current_time = start_time

    while current_time + slot_duration <= end_time:
        if current_time not in booked_times:
            available_slots.append(current_time.strftime('%H:%M'))
        current_time += slot_duration
        
    return {"date": date_str, "slots": available_slots}
