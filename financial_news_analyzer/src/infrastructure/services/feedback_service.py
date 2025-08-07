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
        
        # Debug info
        with st.expander("🔧 Debug - Kayıt Detayları", expanded=False):
            st.write("**Google Sheets Bağlantı Durumu:**")
            if self.gsheet_client:
                st.success("✅ Google Sheets client hazır")
            else:
                st.error("❌ Google Sheets client oluşturulamadı")
                
            sheet_id = st.secrets.get("GOOGLE_SHEET_ID")
            if sheet_id:
                st.success(f"✅ Sheet ID: {sheet_id[:10]}...")
            else:
                st.error("❌ Sheet ID bulunamadı")
                
            credentials = st.secrets.get("gcp_service_account", {})
            if credentials:
                project_id = credentials.get("project_id", "")
                client_email = credentials.get("client_email", "")
                
                if "your-actual" in project_id:
                    st.error("❌ Project ID hala placeholder")
                else:
                    st.success(f"✅ Project ID: {project_id}")
                    
                if "your-service" in client_email:
                    st.error("❌ Client Email hala placeholder")
                else:
                    st.success(f"✅ Client Email: {client_email}")
        
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
            st.error("🔧 Debug: Google Sheets client bulunamadı")
            return False
            
        try:
            spreadsheet_id = st.secrets.get("GOOGLE_SHEET_ID")
            if not spreadsheet_id:
                st.error("🔧 Debug: GOOGLE_SHEET_ID bulunamadı")
                return False
            
            # Check if service account credentials are properly configured
            credentials_dict = st.secrets.get("gcp_service_account", {})
            if not credentials_dict or credentials_dict.get("project_id") == "your-actual-project-id":
                st.error("🔧 Debug: Service account credentials henüz placeholder değerinde")
                return False
            
            st.info(f"🔧 Debug: Sheet ID ile bağlanılıyor: {spreadsheet_id[:10]}...")
            spreadsheet = self.gsheet_client.open_by_key(spreadsheet_id)
            st.success("🔧 Debug: Spreadsheet başarıyla açıldı")
            
            try:
                worksheet = spreadsheet.worksheet("Feedback")
                st.success("🔧 Debug: Feedback worksheet bulundu")
            except Exception as e:
                st.warning(f"🔧 Debug: Feedback worksheet bulunamadı, oluşturuluyor... ({str(e)})")
                worksheet = spreadsheet.add_worksheet(
                    title="Feedback", 
                    rows="1000", 
                    cols="10"
                )
                worksheet.append_row([
                    "Timestamp", "Name", "Email", "Message", "Status"
                ])
                st.success("🔧 Debug: Feedback worksheet oluşturuldu")
            
            # Add the data
            st.info("🔧 Debug: Veri ekleniyor...")
            worksheet.append_row([
                data['timestamp'],
                data['name'], 
                data['email'], 
                data['message'],
                "Yeni"
            ])
            st.success("🔧 Debug: Veri başarıyla Google Sheets'e eklendi!")
            
            return True
            
        except Exception as e:
            st.error(f"🔧 Debug: Google Sheets hatası: {str(e)}")
            import traceback
            st.error(f"🔧 Debug: Detaylı hata: {traceback.format_exc()}")
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
