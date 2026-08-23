from datetime import datetime, timedelta
from app.models import MedicationReminder, User
from app.services.email_service import send_email
from app import db

def process_medication_reminders(app):
    """
    Background job that checks the database for due medication reminders.
    Requires the Flask app context to interact with the database.
    """
    with app.app_context():
        now = datetime.now()
        
        # Find all active reminders where the next_run_at time has passed
        due_reminders = MedicationReminder.query.filter(
            MedicationReminder.status == 'active',
            MedicationReminder.next_run_at <= now
        ).all()

        for reminder in due_reminders:
            patient = User.query.get(reminder.patient_id)
            if patient:
                subject = f"Medication Reminder: {reminder.medication_name}"
                body = f"Hi {patient.name},\n\nIt is time to take your medication: {reminder.medication_name}.\n\nStay healthy!"
                
                # Send the email
                send_email(patient.email, subject, body)
                
                # Update the next run time
                reminder.next_run_at = now + timedelta(hours=reminder.frequency_hours)
                print(f"Reminder sent to {patient.email} for {reminder.medication_name}.")
        
        # Save updates to the database
        if due_reminders:
            db.session.commit()