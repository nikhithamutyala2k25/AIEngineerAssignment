import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")  # Use environment variable for API Key

def send_email_with_sendgrid(subject, to_email, body):
    """Send email using SendGrid API."""
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    from_email = "youremail@example.com"  # Replace with your actual sender email
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    try:
        response = sg.send(message)
        print(f"Email sent to {to_email} with status {response.status_code}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {str(e)}")
