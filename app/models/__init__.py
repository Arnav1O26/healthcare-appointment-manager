from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'admin', 'doctor', or 'patient'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class DoctorProfile(db.Model):
    __tablename__ = 'doctor_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    working_hours_start = db.Column(db.String(5), default='09:00') # HH:MM format
    working_hours_end = db.Column(db.String(5), default='17:00')
    slot_duration_mins = db.Column(db.Integer, default=30)
    
    user = db.relationship('User', backref=db.backref('doctor_profile', uselist=False))

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profiles.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, confirmed, cancelled, completed
    calendar_event_id = db.Column(db.String(100), nullable=True) # For Google Calendar
    
class DoctorLeave(db.Model):
    __tablename__ = 'doctor_leaves'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profiles.id'), nullable=False)
    leave_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(200), nullable=True)