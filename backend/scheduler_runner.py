import threading
from scheduler import send_scheduled_emails

def start_scheduler():
    """Start the scheduler in a separate thread."""
    scheduler_thread = threading.Thread(target=send_scheduled_emails, daemon=True)
    scheduler_thread.start()
