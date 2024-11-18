# AIEngineerAssignment
This project is a Flask-based email management system with features such as Gmail OAuth integration, email scheduling, CSV upload, and analytics. It uses MongoDB for data storage, WebSocket for real-time communication, and Google APIs for sending emails securely. The application provides an intuitive frontend built with HTML, CSS, and JavaScript, ensuring a seamless user experience.

Features:
OAuth 2.0 Gmail Integration: Connect a Gmail account securely to send emails.
CSV Upload: Upload CSV files with recipient data and preview them before processing.
Email Scheduling: Schedule emails to be sent at specific times with MongoDB tracking.
Email Analytics: View statistics for sent, failed, and pending emails, along with detailed status for individual emails.
Real-time Updates: WebSocket integration enables real-time notifications and updates.
Configurable Environment: Environment variables manage sensitive data and application settings.
Technologies Used:
Backend: Python (Flask), MongoDB, Google Gmail API, SendGrid API (optional), Pandas.
Frontend: HTML, CSS, JavaScript.
Real-Time Communication: Socket.IO for WebSocket-based updates.
Project Structure:
Backend: Handles authentication, scheduling, analytics, and real-time communication.
Frontend: Provides a user-friendly dashboard for managing email functionalities.
Environment Variables: Configures API keys, database URIs, and OAuth credentials.
Prerequisites:
Python 3.8 or higher
MongoDB server (local or cloud-based)
Google OAuth credentials (credentials.json) for Gmail integration
