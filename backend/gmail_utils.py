import os
import base64
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    """Authenticate and return Gmail service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = google.auth.load_credentials_from_file('token.json')[0]
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def send_email(service, to, subject, body):
    """Send email via Gmail API."""
    message = create_message('me', to, subject, body)
    send_message(service, 'me', message)

def create_message(sender, to, subject, message_text):
    """Create email message."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_message(service, sender, message):
    """Send email message via Gmail."""
    try:
        message = service.users().messages().send(userId=sender, body=message).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
