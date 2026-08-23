import os
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Note: For this to work in production, you need a 'token.json' file generated 
# by a full Google OAuth 2.0 flow. 

def get_calendar_service():
    """Authenticates and returns the Google Calendar API service."""
    creds = None
    # We will look for a saved token file
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    
    if not creds or not creds.valid:
        print("Google Calendar not authenticated. Skipping calendar sync.")
        return None
        
    return build('calendar', 'v3', credentials=creds)

def create_calendar_event(summary, description, start_time_str, end_time_str, patient_email, doctor_email):
    """
    Creates a calendar event for both the doctor and the patient.
    Time strings should be in ISO format: '2026-08-23T09:00:00+05:30'
    """
    service = get_calendar_service()
    if not service:
        return {"success": False, "message": "Calendar service unavailable"}

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time_str,
            'timeZone': 'Asia/Kolkata', # Defaulting to IST based on current timezone
        },
        'end': {
            'dateTime': end_time_str,
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [
            {'email': patient_email},
            {'email': doctor_email},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }

    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return {"success": True, "event_link": event_result.get('htmlLink'), "event_id": event_result.get('id')}
    except HttpError as error:
        print(f"An error occurred with Google Calendar: {error}")
        return {"success": False, "error": str(error)}