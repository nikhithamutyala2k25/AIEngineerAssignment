import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.smtp_settings import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

def send_email_smtp(to_email, subject, body):
    """Send email using SMTP."""
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
