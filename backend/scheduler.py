# from config.database import email_schedules  # Import the email_schedules collection
# from config.settings import SENDGRID_API_KEY, FROM_EMAIL  # Access settings
# from datetime import datetime
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# import time

# def send_scheduled_emails():
#     """Poll MongoDB for emails that need to be sent, and send them."""
#     while True:
#         current_time = datetime.utcnow()
#         emails_to_send = email_schedules.find({
#             "send_time": {"$lte": current_time},
#             "status": "scheduled"
#         })

#         for email in emails_to_send:
#             sg = SendGridAPIClient(SENDGRID_API_KEY)
#             message = Mail(
#                 from_email=FROM_EMAIL,
#                 to_emails=email["to_email"],
#                 subject=email["subject"],
#                 plain_text_content=email["content"]
#             )

#             try:
#                 sg.send(message)
#                 email_schedules.update_one(
#                     {"_id": email["_id"]},
#                     {"$set": {"status": "sent"}}
#                 )
#                 print(f"Email sent to {email['to_email']}")
#             except Exception as e:
#                 email_schedules.update_one(
#                     {"_id": email["_id"]},
#                     {"$set": {"status": "failed", "error": str(e)}}
#                 )
#                 print(f"Failed to send email to {email['to_email']}")

#         # Wait for a minute before checking again
#         time.sleep(60)
# def generate_and_send_email(data, template, send_email_function):
#     email_content = generate_email_content(template, data)
#     send_email_function(data['email'], "Custom Subject", email_content)
import threading
import time
from sendgrid_utils import send_email_with_sendgrid
from gmail_utils import send_email as send_email_gmail


from smtp_utils import send_email_smtp
from datetime import datetime
from config.database import email_schedules  # Import MongoDB collection
from config.settings import SENDGRID_API_KEY, FROM_EMAIL  # Settings file for API key and from email
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

EMAIL_STATUSES = {}

def schedule_emails(email_data, subject, body_template, delay=0, email_service='sendgrid'):
    """Schedule emails with optional delay between them."""
    for idx, email_info in enumerate(email_data):
        # Generate dynamic email body
        body = body_template.format(**email_info)
        
        # Schedule email sending with delay
        threading.Timer(delay * idx, send_email, [email_service, email_info['Email'], subject, body]).start()

def send_email(email_service, to_email, subject, body):
    """Send email using the specified email service."""
    if email_service == 'sendgrid':
        send_email_with_sendgrid(subject, to_email, body)
    elif email_service == 'gmail':
        service = gmail_authenticate()  # Authenticate Gmail
        send_email_gmail(service, to_email, subject, body)
    elif email_service == 'smtp':
        send_email_smtp(to_email, subject, body)

def generate_email_content(template, data):
    """Generate email content with dynamic placeholders."""
    for key, value in data.items():
        template = template.replace(f"{{{key}}}", value)
    return template

def send_scheduled_emails():
    """Poll MongoDB for emails that need to be sent, and send them."""
    while True:
        current_time = datetime.utcnow()
        emails_to_send = email_schedules.find({
            "send_time": {"$lte": current_time},
            "status": "scheduled"
        })

        for email in emails_to_send:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            message = Mail(
                from_email=FROM_EMAIL,
                to_emails=email["to_email"],
                subject=email["subject"],
                plain_text_content=email["content"]
            )

            try:
                sg.send(message)
                email_schedules.update_one(
                    {"_id": email["_id"]},
                    {"$set": {"status": "sent"}}
                )
                print(f"Email sent to {email['to_email']}")
            except Exception as e:
                email_schedules.update_one(
                    {"_id": email["_id"]},
                    {"$set": {"status": "failed", "error": str(e)}}
                )
                print(f"Failed to send email to {email['to_email']}")

        # Wait for a minute before checking again
        time.sleep(60)
