# import os
# from dotenv import load_dotenv

# # Load environment variables from the .env file
# load_dotenv()

# # Access environment variables
# SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
# FROM_EMAIL = os.getenv("FROM_EMAIL", "default_email@example.com")  # Set a default if it's not in the .env file

# # Additional Flask settings
# FLASK_APP = os.getenv("FLASK_APP", "app.py")
# FLASK_DEBUG = os.getenv("FLASK_DEBUG", "1")  # Default is "1", meaning debug mode is on

# # You can print the variables to verify
# print(f"SendGrid API Key: {SENDGRID_API_KEY}")
# print(f"From Email: {FROM_EMAIL}")
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Environment variables
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "youremai@gmail.com")  # Default value if missing
MONGO_URI = os.getenv("MONGO_URI")  # MongoDB connection string

# Additional Flask settings
FLASK_APP = os.getenv("FLASK_APP", "app.py")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "1")  # Debug mode default: on

# Debug prints for confirmation
print(f"SENDGRID_API_KEY: {SENDGRID_API_KEY}")
print(f"FROM_EMAIL: {FROM_EMAIL}")
print(f"MONGO_URI: {MONGO_URI}")
