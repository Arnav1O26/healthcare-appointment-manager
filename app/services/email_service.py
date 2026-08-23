import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    """
    Sends an email using standard SMTP.
    Requires SMTP_EMAIL and SMTP_PASSWORD in the .env file.
    """
    sender_email = os.getenv('SMTP_EMAIL')
    sender_password = os.getenv('SMTP_PASSWORD')

    if not sender_email or not sender_password:
        print("Email credentials not configured. Skipping email send.")
        return {"success": False, "message": "Credentials missing"}

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Using Gmail's SMTP server as the default
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return {"success": True, "message": "Email sent!"}
    except Exception as e:
        print(f"Failed to send email: {e}")
        return {"success": False, "error": str(e)}

def send_booking_confirmation(patient_email, doctor_name, date, time):
    subject = "Appointment Confirmed!"
    body = f"Your appointment with {doctor_name} on {date} at {time} is confirmed.\n\nPlease arrive 5 minutes early."
    return send_email(patient_email, subject, body)