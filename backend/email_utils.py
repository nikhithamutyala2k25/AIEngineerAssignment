import os
import threading
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import GOOGLE_CREDENTIALS_FILE
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

# Store email statuses
EMAIL_STATUSES = {}

# Retrieve SendGrid API key from environment variable (or replace with your actual key)
SENDGRID_API_KEY = os.getenv("
sendgridapikey", "YOUR_ACTUAL_API_KEY")  # Replace with your actual SendGrid API key

def send_email(subject, to_email, body):
    """
    Sends a single email using SendGrid API.
    """
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    from_email = "21wh1a05f2@bvrithyderabad.edu.in"  # Replace with your actual sender's email
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    try:
        response = sg.send(message)
        EMAIL_STATUSES[to_email] = "Sent"  # Track status
        print(f"Email sent to {to_email} with status {response.status_code}")
    except Exception as e:
        EMAIL_STATUSES[to_email] = f"Failed: {str(e)}"
        print(f"Error sending email to {to_email}: {str(e)}")

def schedule_emails(email_data, subject, prompt, delay=0):
    """
    Schedules emails to be sent with optional delay.
    """
    for idx, email_info in enumerate(email_data):
        # Format message using prompt
        body = prompt.format(**email_info)
        # Schedule email to be sent with delay
        threading.Timer(delay * idx, send_email, [subject, email_info['Email'], body]).start()

def connect_gmail_account():
    flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS_FILE, ['https://www.googleapis.com/auth/gmail.send'])
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service
def send_email_smtp(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USER, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
def generate_email_content(template, data):
    for key, value in data.items():
        template = template.replace(f"{{{key}}}", value)
    return template


# Example usage
if __name__ == "__main__":
    # Example data
    email_data = [
        {"Email": "email1@example.com", "Company Name": "Company A", "Location": "New York"},
        {"Email": "email2@example.com", "Company Name": "Company B", "Location": "San Francisco"},
    ]
    prompt = "Hello {Company Name}, we are excited to reach out to you in {Location}."
    subject = "Exciting News from Our Company"
    
    # Schedule emails with a delay of 5 seconds between each
    schedule_emails(email_data, subject, prompt, delay=5)
    
    # Allow time for threads to complete (for testing)
    time.sleep(10)
    print(EMAIL_STATUSES)

