from flask import jsonify
from database.models import email_status_collection

@app.route('/analytics', methods=['GET'])
def analytics():
    # Fetch the counts of different email statuses
    sent_count = email_status_collection.count_documents({"status": "sent"})
    failed_count = email_status_collection.count_documents({"status": "failed"})
    scheduled_count = email_status_collection.count_documents({"status": "scheduled"})
    
    # Fetch the email status data
    email_status_data = list(email_status_collection.find({}))
    
    # Prepare the data for the response
    data = {
        "sent": sent_count,
        "failed": failed_count,
        "scheduled": scheduled_count,
        "emailStatuses": []
    }
    
    # Process each email status and include deliveryStatus and opened fields
    for email in email_status_data:
        email_status = {
            "email": email.get('email', 'N/A'),
            "status": email.get('status', 'N/A'),
            "deliveryStatus": email.get('deliveryStatus', 'N/A'),  # Default to 'N/A' if not present
            "opened": email.get('opened', 'N/A')  # Default to 'N/A' if not present
        }
        data['emailStatuses'].append(email_status)
    
    # Return the response in JSON format
    return jsonify(data)
