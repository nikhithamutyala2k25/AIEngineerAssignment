from pymongo import MongoClient
from datetime import datetime
import pytz
from marshmallow import Schema, fields, post_load

# MongoDB Client Setup (assuming a local MongoDB instance)
MONGO_URI = "mongodb://localhost:27017/emailApp"
client = MongoClient(MONGO_URI)
db = client["email_dashboard"]

# Defining the EmailStatus model
class EmailStatus:
    def __init__(self, email, status, error=None):
        self.email = email
        self.status = status
        self.error = error
        self.timestamp = datetime.now(pytz.utc)

    def save(self):
        """Save the email status to the MongoDB collection"""
        email_status_collection = db["statuses"]
        email_status_collection.insert_one(self.__dict__)

# Defining the ScheduledEmail model
class ScheduledEmail:
    def __init__(self, subject, to_email, from_email, content, send_time, status="scheduled"):
        self.subject = subject
        self.to_email = to_email
        self.from_email = from_email
        self.content = content
        self.send_time = send_time
        self.status = status

    def save(self):
        """Save the scheduled email to the MongoDB collection"""
        email_schedule_collection = db["email_schedules"]
        email_schedule_collection.insert_one(self.__dict__)

# Marshmallow Schemas for serialization (optional, if you want to serialize data)
class EmailStatusSchema(Schema):
    email = fields.Str(required=True)
    status = fields.Str(required=True)
    error = fields.Str()
    timestamp = fields.DateTime()

    @post_load
    def make_email_status(self, data, **kwargs):
        return EmailStatus(**data)

class ScheduledEmailSchema(Schema):
    subject = fields.Str(required=True)
    to_email = fields.Str(required=True)
    from_email = fields.Str(required=True)
    content = fields.Str(required=True)
    send_time = fields.DateTime(required=True)
    status = fields.Str()

    @post_load
    def make_scheduled_email(self, data, **kwargs):
        return ScheduledEmail(**data)

# Utility functions (optional)
def get_all_email_statuses():
    """Retrieve all email statuses from the database"""
    email_status_collection = db["statuses"]
    return email_status_collection.find()

def get_all_scheduled_emails():
    """Retrieve all scheduled emails from the database"""
    email_schedule_collection = db["email_schedules"]
    return email_schedule_collection.find()
