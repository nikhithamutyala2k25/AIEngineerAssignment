from pymongo import MongoClient
import pandas as pd
import os
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth.exceptions
import pickle
from flask import request, jsonify
from flask import Flask, redirect, url_for, session
from google_auth_oauthlib.flow import Flow
from flask_cors import CORS
from datetime import datetime, timedelta
import pytz, secrets
from scheduler import send_scheduled_emails  # Ensure you have this function defined in scheduler.py
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Initialize Flask app and enable CORS
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
# Set a secret key
app.secret_key = secrets.token_hex(24)
CORS(app)

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/emailApp")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["email_dashboard"]
email_statuses = db["statuses"]
email_schedules = db["email_schedules"]

# SendGrid API Key
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
if not SENDGRID_API_KEY:
    raise ValueError("SENDGRID_API_KEY not found in environment variables.")

@app.route('/')
def home():
    return "Email Scheduler App is Running!"

# Handle WebSocket connections
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'message': 'Connected to the server'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

# Define environment variables for OAuth
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # For local testing
CLIENT_SECRETS_FILE = "credentials.json"

# Set up OAuth 2.0 flow
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=["https://www.googleapis.com/auth/gmail.send"],
    redirect_uri="http://localhost:5000/gmail_callback"  # Adjust for your domain
)

@app.route('/connect_gmail')
def connect_gmail():
    # Generate the authorization URL
    auth_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    session["state"] = state  # Save the state in the session for verification
    return redirect(auth_url)

@app.route('/gmail_callback')
def gmail_callback():
    # Debug: Print the incoming URL
    print("Incoming callback URL:", request.url)
    
    # Initialize the OAuth flow with the correct credentials file and redirect URI
    flow = Flow.from_client_secrets_file(
        'credentials.json',  # Path to credentials.json (now in the root directory)
        scopes=["https://www.googleapis.com/auth/gmail.send"],
        redirect_uri='http://localhost:5000/gmail_callback'  # Ensure this is the correct redirect URI
    )

    try:
        # Fetch the token using the authorization response
        flow.fetch_token(authorization_response=request.url)
        
        # Store the credentials in the session
        credentials = flow.credentials
        session['credentials'] = credentials_to_dict(credentials)
        
        return "Token fetched successfully!"

    except Exception as e:
        return f"Error during token fetch: {e}"

def credentials_to_dict(credentials):
    """Convert credentials object to a serializable dictionary."""
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

# Upload CSV endpoint

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        df = df.applymap(lambda x: x.strip().replace('"', '') if isinstance(x, str) else x)
        preview = df.head().to_dict(orient="records")
        return jsonify({"columns": df.columns.tolist(), "preview": preview})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper: Replace placeholders in the email content with actual values
def replace_placeholders(content, data):
    content = content.replace("[First Name]", data.get("firstName", "User"))
    content = content.replace("[Email]", data.get("email", "N/A"))
    return content

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.json
    subject = data.get("subject")
    to_email = data.get("to_email")
    content = data.get("content")

    if "credentials" not in session:
        return jsonify({"error": "Gmail account not connected."}), 400

    credentials = session["credentials"]
    try:
        service = build("gmail", "v1", credentials=credentials)
        mime_message = MIMEText(content)
        mime_message["to"] = to_email
        mime_message["subject"] = subject

        raw_message = urlsafe_b64encode(mime_message.as_bytes()).decode()
        message = {"raw": raw_message}

        sent_message = service.users().messages().send(userId="me", body=message).execute()
        return jsonify({"message": "Email sent successfully!", "id": sent_message["id"]})
    except HttpError as error:
        return jsonify({"error": str(error)}), 500




@app.route('/analytics', methods=['GET'])
def analytics():
    # Count sent, failed, and bounced emails
    sent_count = email_statuses.count_documents({"status": "sent"})
    failed_count = email_statuses.count_documents({"status": "failed"})
    bounced_count = email_statuses.count_documents({"deliveryStatus": "bounced"})
    
    # Fetch email statuses and other details
    email_status_data = list(email_statuses.find({}))
    
    # Prepare data to send as response
    data = {
        "sent": sent_count,
        "failed": failed_count,
        "bounced": bounced_count,
        "emailStatuses": [{
            "email": email['email'],
            "status": email['status'],
            "deliveryStatus": email.get("deliveryStatus", "N/A"),
            "opened": email.get("opened", "N/A")
        } for email in email_status_data]
    }
    
    return jsonify(data)


# Start scheduler in a background thread
def start_scheduler():
    print("Starting the scheduler in the background...")
    scheduler_thread = Thread(target=send_scheduled_emails, daemon=True)
    scheduler_thread.start()

@app.route('/start_scheduler', methods=['POST'])
def start_scheduler_endpoint():
    start_scheduler()
    return jsonify({"message": "Scheduler started successfully!"}), 200

# Schedule email endpoint
@app.route('/schedule_email', methods=['POST'])
def schedule_email():
    data = request.json
    subject = data.get("subject")
    to_email = data.get("to_email")
    from_email = data.get("from_email")
    content = data.get("content")

    if not all([subject, to_email, from_email, content]):
        return jsonify({"error": "Missing required fields."}), 400

    current_time = datetime.now(pytz.utc)
    next_minute = current_time + timedelta(minutes=1)
    next_minute = next_minute.replace(second=0, microsecond=0)

    email_schedules.insert_one({
        "subject": subject,
        "to_email": to_email,
        "from_email": from_email,
        "content": content,
        "send_time": next_minute,
        "status": "scheduled"
    })

    return jsonify({"message": f"Email scheduled to {to_email} at {next_minute}"}), 200

# Run the app
if __name__ == "__main__":
    socketio.run(app, debug=True)
