import os
import csv
from datetime import datetime
import firebase_admin  # type: ignore
from firebase_admin import credentials, firestore  # type: ignore
import streamlit as st  # type: ignore  # only for reading secrets


class FeedbackService:
    """
    Service for saving user feedback to Firestore with CSV fallback.
    """

    def __init__(self, secrets: dict):
        self.secrets = secrets

        # Initialize Firebase App once
        if not firebase_admin._apps:
            # Load Firebase service account credentials from passed secrets
            creds_dict = self.secrets.get("gcp_service_account")
            creds = credentials.Certificate(creds_dict)
            firebase_admin.initialize_app(creds)

        # Firestore client
        self.db = firestore.client()

        # Prepare local CSV fallback path
        self.csv_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(self.csv_dir, exist_ok=True)
        self.csv_file = os.path.join(self.csv_dir, "feedback.csv")

    def save(self, name: str, email: str, message: str) -> None:
        """
        Save feedback to Firestore; on failure, append to local CSV.
        """
        timestamp = datetime.utcnow().isoformat()
        data = {
            "timestamp": timestamp,
            "name": name,
            "email": email,
            "message": message
        }

        # Get Firestore collection name from secrets
        collection = self.secrets.get("db_collection", "feedback")

        try:
            # Attempt to write to Firestore
            self.db.collection(collection).add(data)
        except Exception:
            # Fallback to local CSV storage on any error
            file_exists = os.path.exists(self.csv_file)
            with open(self.csv_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Timestamp", "Name", "Email", "Message"])
                writer.writerow([timestamp,
