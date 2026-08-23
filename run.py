from app import create_app, db
from app.models import User, DoctorProfile, Appointment, MedicationReminder
from app.services.scheduler_service import process_medication_reminders
from flask_apscheduler import APScheduler

app = create_app()
scheduler = APScheduler()

# Configure the scheduler
scheduler.init_app(app)

# Schedule the reminder job to run every 5 minutes
@scheduler.task('interval', id='medication_job', minutes=5)
def scheduled_task():
    print("Running background check for medication reminders...")
    process_medication_reminders(app)

scheduler.start()

# For the Flask shell
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 'User': User, 'DoctorProfile': DoctorProfile, 
        'Appointment': Appointment, 'MedicationReminder': MedicationReminder
    }

if __name__ == '__main__':
    # use_reloader=False prevents the scheduler from running twice in debug mode
    app.run(debug=True, use_reloader=False)