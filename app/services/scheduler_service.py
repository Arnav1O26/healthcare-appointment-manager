from datetime import datetime, timedelta
from app import db
from app.models import MedicationReminder, User
from app.services.email_service import send_email

def check_medication_reminders(app):
    """
    Background job to process due medication reminders.
    Requires the Flask app instance to access the database context.
    """
    with app.app_context():
        now = datetime.now()
        # Find all active reminders that are due to be sent
        due_reminders = MedicationReminder.query.filter(
            MedicationReminder.status == 'active',
            MedicationReminder.next_run_at <= now
        ).all()
        
        for reminder in due_reminders:
            patient = User.query.get(reminder.patient_id)
            if patient:
                # 1. Send the email
                subject = "Medication Reminder"
                body = f"Hello {patient.name},\n\nIt is time to take your medication: {reminder.medication_name}.\n\nPlease stay on schedule!\n\n- Clinic Admin"
                send_email(patient.email, subject, body)
                
                # 2. Update the next run time
                reminder.next_run_at = now + timedelta(hours=reminder.frequency_hours)
                
        db.session.commit()