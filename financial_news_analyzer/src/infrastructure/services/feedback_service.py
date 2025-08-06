import os
import csv
from datetime import datetime
try:
    import firebase_admin  # type: ignore
    from firebase_admin import credentials, firestore  # type: ignore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
import streamlit as st # type: ignore


class FeedbackService:
    """
    Service for saving user feedback to Firestore with CSV fallback.
    """
    def __init__(self, secrets: dict):
        self.secrets = secrets
        # Initialize Firestore client if available
        if FIREBASE_AVAILABLE:
            try:
                if not firebase_admin._apps:
                    creds_dict = st.secrets.get("gcp_service_account", {})
                    creds = credentials.Certificate(creds_dict)
                    firebase_admin.initialize_app(creds)
                self.db = firestore.client()
            except Exception:
                self.db = None
        else:
            self.db = None
        # Prepare local CSV path
        self.csv_dir = os.path.join(os.getcwd(), 'data')
        os.makedirs(self.csv_dir, exist_ok=True)
        self.csv_file = os.path.join(self.csv_dir, 'feedback.csv')

    def save(self, name: str, email: str, message: str) -> None:
        """
        Save feedback to Firestore; on failure, append to local CSV.
        """
        timestamp = datetime.utcnow().isoformat()
        data = {
            'timestamp': timestamp,
            'name': name,
            'email': email,
            'message': message
        }
        # Attempt to store in Firestore if client initialized
        if self.db:
            try:
                collection = st.secrets.get("FIRESTORE_COLLECTION", "feedback")
                self.db.collection(collection).add(data)
                return
            except Exception:
                pass
        # Fallback to CSV storage
        file_exists = os.path.exists(self.csv_file)
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Timestamp', 'Name', 'Email', 'Message'])
            writer.writerow([timestamp, name, email, message])
