import os
import csv
from datetime import datetime

try:
    import gspread  # type: ignore
    from google.oauth2.service_account import Credentials  # type: ignore
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

import streamlit as st # type: ignore


class FeedbackService:
    """
    Service for saving user feedback to Google Sheets with CSV fallback.
    Priority: Google Sheets -> CSV
    """
    def __init__(self, secrets: dict):
        self.secrets = secrets
        self.gsheet_client = None
        
        # Initialize Google Sheets client
        if GSPREAD_AVAILABLE:
            self._init_google_sheets()
        
        # Prepare local CSV path as final fallback
        self.csv_dir = os.path.join(os.getcwd(), 'data')
        os.makedirs(self.csv_dir, exist_ok=True)
        self.csv_file = os.path.join(self.csv_dir, 'feedback.csv')

    def _init_google_sheets(self):
        """Initialize Google Sheets client."""
        try:
            credentials_dict = st.secrets.get("gcp_service_account", {})
            if not credentials_dict:
                print("DEBUG: gcp_service_account secrets bulunamadı")
                return
            
            # Check for placeholder values
            project_id = credentials_dict.get("project_id", "")
            client_email = credentials_dict.get("client_email", "")
            private_key = credentials_dict.get("private_key", "")
            
            if (project_id == "your-actual-project-id" or 
                "your-project" in client_email or 
                "YOUR_ACTUAL_PRIVATE_KEY" in private_key):
                print("DEBUG: Service account credentials henüz placeholder değerlerinde")
                return
                
            print("DEBUG: Credentials dict bulundu ve placeholder değil")
            
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            
            credentials = Credentials.from_service_account_info(
                credentials_dict, 
                scopes=scope
            )
            
            print("DEBUG: Credentials oluşturuldu")
            
            self.gsheet_client = gspread.authorize(credentials)
            print("DEBUG: gspread client oluşturuldu")
            
        except Exception as e:
            print(f"DEBUG: Google Sheets init hatası: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            self.gsheet_client = None

    def save(self, name: str, email: str, message: str) -> bool:
        """
        Save feedback with Google Sheets and CSV fallback.
        Priority: Google Sheets -> CSV
        
        Returns:
            bool: True if saved successfully to any backend
        """
        if not name or not email or not message:
            st.warning("Lütfen tüm alanları doldurun.")
            return False
            
        timestamp = datetime.utcnow().isoformat()
        data = {
            'timestamp': timestamp,
            'name': name,
            'email': email,
            'message': message
        }
        
        # Show what we're trying first
        st.info("💾 Mesaj kaydediliyor...")
        
        # Try Google Sheets first
        if self._save_to_google_sheets(data):
            st.success("✅ Mesajınız Google Sheets'e başarıyla kaydedildi!")
            return True
        
        # Use CSV as fallback
        if self._save_to_csv(data):
            st.success("✅ Mesajınız başarıyla kaydedildi!")
            st.info("� Mesajlar CSV dosyasında güvenle saklanıyor.")
            return True
        
        st.error("❌ Mesaj kaydedilemedi. Lütfen daha sonra tekrar deneyin.")
        return False

    def _save_to_google_sheets(self, data: dict) -> bool:
        """Save to Google Sheets."""
        if not self.gsheet_client:
            print("DEBUG: gsheet_client None")
            return False
            
        try:
            spreadsheet_id = st.secrets.get("GOOGLE_SHEET_ID")
            if not spreadsheet_id:
                print("DEBUG: GOOGLE_SHEET_ID bulunamadı")
                return False
            
            # Check if service account credentials are properly configured
            credentials_dict = st.secrets.get("gcp_service_account", {})
            if not credentials_dict or credentials_dict.get("project_id") == "your-actual-project-id":
                print("DEBUG: Service account credentials henüz yapılandırılmamış")
                return False
            
            print(f"DEBUG: Sheet ID: {spreadsheet_id}")
            spreadsheet = self.gsheet_client.open_by_key(spreadsheet_id)
            print("DEBUG: Spreadsheet açıldı")
            
            try:
                worksheet = spreadsheet.worksheet("Feedback")
                print("DEBUG: Feedback worksheet bulundu")
            except Exception as e:
                print(f"DEBUG: Feedback worksheet bulunamadı, oluşturuluyor: {e}")
                worksheet = spreadsheet.add_worksheet(
                    title="Feedback", 
                    rows="1000", 
                    cols="10"
                )
                worksheet.append_row([
                    "Timestamp", "Name", "Email", "Message", "Status"
                ])
                print("DEBUG: Feedback worksheet oluşturuldu")
            
            # Add the data
            worksheet.append_row([
                data['timestamp'],
                data['name'], 
                data['email'], 
                data['message'],
                "Yeni"
            ])
            print("DEBUG: Veri başarıyla eklendi")
            
            return True
            
        except Exception as e:
            print(f"DEBUG: Google Sheets hatası: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            return False

    def _save_to_csv(self, data: dict) -> bool:
        """Save to CSV file."""
        try:
            file_exists = os.path.exists(self.csv_file)
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['Timestamp', 'Name', 'Email', 'Message'])
                writer.writerow([
                    data['timestamp'], 
                    data['name'], 
                    data['email'], 
                    data['message']
                ])
            return True
        except Exception:
            return False
