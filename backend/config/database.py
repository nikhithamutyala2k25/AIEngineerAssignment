from pymongo import MongoClient
from config.settings import MONGO_URI

# Initialize MongoDB client
client = MongoClient(MONGO_URI)

# Select database and collection
db = client["email_scheduler_db"]  # Replace with your database name
email_schedules = db["email_schedules"]  # Replace with your collection name

# Debug print to confirm connection
print("Connected to MongoDB!")
from pymongo import MongoClient
from config.settings import MONGO_URI

# Initialize MongoDB client
client = MongoClient(MONGO_URI)

# Select database and collection
db = client["email_scheduler_db"]  # Replace with your database name
email_schedules = db["email_schedules"]  # Replace with your collection name

# Debug print to confirm connection
print("Connected to MongoDB!")
