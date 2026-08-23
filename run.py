from app import create_app, db
from app.models import User, DoctorProfile, Appointment

app = create_app()

# This context processor makes the db and models available in the Flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'DoctorProfile': DoctorProfile, 'Appointment': Appointment}

if __name__ == '__main__':
    app.run(debug=True)