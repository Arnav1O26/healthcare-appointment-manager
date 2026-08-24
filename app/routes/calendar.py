import os
from flask import Blueprint, redirect, request, session, url_for, flash
from google_auth_oauthlib.flow import Flow

calendar_bp = Blueprint('calendar', __name__)

# This MUST match the URI you pasted in Google Cloud exactly
REDIRECT_URI = 'http://localhost:5000/oauth2callback'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# This allows OAuth to run over HTTP (localhost) instead of requiring HTTPS
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@calendar_bp.route('/connect-calendar')
def connect_calendar():
    """Generates the Google login URL and redirects the user there."""
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    # Save the state AND the new code_verifier to verify the callback
    session['state'] = state
    session['code_verifier'] = flow.code_verifier
    
    return redirect(authorization_url)

@calendar_bp.route('/oauth2callback')
def oauth2callback():
    """Google redirects the user back to this route after they log in."""
    state = session.get('state')
    
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )
    
    # Retrieve the code_verifier we saved before the user left
    flow.code_verifier = session.get('code_verifier')
    
    # Exchange the authorization code for actual access credentials
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    
    # Store the credentials in the Flask session dictionary
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    flash('Google Calendar connected successfully!', 'success')
    return redirect(url_for('patient.dashboard'))