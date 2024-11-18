import os
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.sendgrid.net")  # Or another SMTP server
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "apikey")  # For SendGrid, always use 'apikey'
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your-sendgrid-api-key")