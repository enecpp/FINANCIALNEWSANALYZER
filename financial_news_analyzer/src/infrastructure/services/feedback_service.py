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

# Import GitHub feedback service
try:
    from .github_feedback_service import GitHubFeedbackService
    GITHUB_FEEDBACK_AVAILABLE = True
except ImportError:
    GITHUB_FEEDBACK_AVAILABLE = False


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
        """Initialize Google Sheets client with comprehensive error handling."""
        print("DEBUG: Google Sheets client initialization başlıyor...")
        
        try:
            # Check gspread availability
            if not GSPREAD_AVAILABLE:
                print("DEBUG: gspread kütüphanesi bulunamadı")
                return
                
            print("DEBUG: gspread kütüphanesi mevcut")
            
            # Get credentials from secrets
            credentials_dict = st.secrets.get("gcp_service_account", {})
            if not credentials_dict:
                print("DEBUG: gcp_service_account secrets bulunamadı")
                return
            
            print("DEBUG: gcp_service_account secrets bulundu")
            
            # Validate credential fields
            required_fields = ["type", "project_id", "private_key_id", "private_key", 
                             "client_email", "client_id", "auth_uri", "token_uri"]
            
            missing_fields = [field for field in required_fields if not credentials_dict.get(field)]
            if missing_fields:
                print(f"DEBUG: Eksik credential alanları: {missing_fields}")
                return
                
            print("DEBUG: Tüm gerekli credential alanları mevcut")
            
            # Check for placeholder values
            project_id = credentials_dict.get("project_id", "")
            client_email = credentials_dict.get("client_email", "")
            private_key = credentials_dict.get("private_key", "")
            
            if (project_id == "your-actual-project-id" or 
                "your-project" in client_email or 
                "YOUR_ACTUAL_PRIVATE_KEY" in private_key):
                print("DEBUG: Service account credentials henüz placeholder değerlerinde")
                return
                
            print(f"DEBUG: Project ID: {project_id}")
            print(f"DEBUG: Client Email: {client_email}")
            print(f"DEBUG: Private Key mevcut: {'private_key' in credentials_dict}")
            
            # Validate private key format
            if not private_key.startswith("-----BEGIN PRIVATE KEY-----"):
                print("DEBUG: Private key formatı geçersiz - BEGIN marker eksik")
                return
                
            if not private_key.endswith("-----END PRIVATE KEY-----\n"):
                print("DEBUG: Private key formatı geçersiz - END marker eksik")
                # Try to fix the format
                if not private_key.endswith("\n"):
                    credentials_dict["private_key"] = private_key + "\n"
                    print("DEBUG: Private key formatı düzeltildi")
                    
            print("DEBUG: Private key formatı geçerli")
            
            # Create scopes
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.file'
            ]
            
            print(f"DEBUG: Scope ayarlandı: {scope}")
            
            # Create credentials step by step
            print("DEBUG: Credentials oluşturuluyor...")
            credentials = Credentials.from_service_account_info(
                credentials_dict, 
                scopes=scope
            )
            
            if not credentials:
                print("DEBUG: Credentials oluşturulamadı")
                return
                
            print("DEBUG: Credentials başarıyla oluşturuldu")
            print(f"DEBUG: Credentials valid: {credentials.valid}")
            print(f"DEBUG: Credentials expired: {credentials.expired}")
            
            # Try to refresh credentials if needed
            if credentials.expired:
                print("DEBUG: Credentials süresi dolmuş, yenileniyor...")
                try:
                    credentials.refresh()
                    print("DEBUG: Credentials başarıyla yenilendi")
                except Exception as refresh_error:
                    print(f"DEBUG: Credentials yenilenemedi: {str(refresh_error)}")
                    return
            
            # Authorize with gspread
            print("DEBUG: gspread authorization başlıyor...")
            self.gsheet_client = gspread.authorize(credentials)
            
            if not self.gsheet_client:
                print("DEBUG: gspread client oluşturulamadı")
                return
                
            print("DEBUG: gspread client başarıyla oluşturuldu")
            
            # Test connection with specific error handling
            try:
                test_sheet_id = st.secrets.get("GOOGLE_SHEET_ID")
                if not test_sheet_id:
                    print("DEBUG: GOOGLE_SHEET_ID bulunamadı")
                    return
                    
                print(f"DEBUG: Test sheet ID: {test_sheet_id}")
                print("DEBUG: Test bağlantısı deneniyor...")
                
                test_sheet = self.gsheet_client.open_by_key(test_sheet_id)
                print(f"DEBUG: Test bağlantısı başarılı - Sheet title: {test_sheet.title}")
                
                # Test worksheet access
                worksheets = test_sheet.worksheets()
                print(f"DEBUG: Mevcut worksheets: {[ws.title for ws in worksheets]}")
                
            except Exception as test_e:
                print(f"DEBUG: Test bağlantısı başarısız: {str(test_e)}")
                print(f"DEBUG: Test error type: {type(test_e).__name__}")
                
                # Keep client even if test fails - might be sheet access issue
                if "not found" in str(test_e).lower():
                    print("DEBUG: Sheet bulunamadı ama client çalışıyor olabilir")
                elif "permission" in str(test_e).lower():
                    print("DEBUG: İzin hatası - Service account'a sheet erişimi verilmeli")
                    self.gsheet_client = None
                else:
                    print("DEBUG: Bilinmeyen test hatası - client temizleniyor")
                    self.gsheet_client = None
            
        except ImportError as ie:
            print(f"DEBUG: Import hatası: {str(ie)}")
            self.gsheet_client = None
        except Exception as e:
            print(f"DEBUG: Google Sheets init genel hatası: {str(e)}")
            print(f"DEBUG: Error type: {type(e).__name__}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            self.gsheet_client = None
            
        # Final status
        if self.gsheet_client:
            print("DEBUG: Google Sheets client initialization BAŞARILI ✅")
        else:
            print("DEBUG: Google Sheets client initialization BAŞARISIZ ❌")

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
        with st.expander("🔧 Debug - Kayıt Detayları", expanded=True):
            st.write("**Google Sheets Bağlantı Durumu:**")
            if self.gsheet_client:
                st.success("✅ Google Sheets client hazır")
                
                # Test bağlantı
                try:
                    sheet_id = st.secrets.get("GOOGLE_SHEET_ID")
                    if sheet_id:
                        test_sheet = self.gsheet_client.open_by_key(sheet_id)
                        st.success(f"✅ Test bağlantısı başarılı: {test_sheet.title}")
                        
                        # Show worksheets
                        worksheets = test_sheet.worksheets()
                        ws_names = [ws.title for ws in worksheets]
                        st.info(f"📊 Mevcut worksheets: {', '.join(ws_names)}")
                        
                    else:
                        st.error("❌ Sheet ID bulunamadı")
                except Exception as e:
                    st.error(f"❌ Sheet bağlantı testi başarısız: {str(e)}")
                    
            else:
                st.error("❌ Google Sheets client oluşturulamadı")
                st.info("🔧 **Detaylı Tanı:**")
                
                # Check gspread availability
                if GSPREAD_AVAILABLE:
                    st.success("✅ gspread kütüphanesi mevcut")
                else:
                    st.error("❌ gspread kütüphanesi bulunamadı")
                    
                # Check secrets
                credentials = st.secrets.get("gcp_service_account", {})
                if credentials:
                    st.success("✅ Service account secrets mevcut")
                    
                    # Check required fields
                    required_fields = ["type", "project_id", "private_key_id", "private_key", 
                                     "client_email", "client_id", "auth_uri", "token_uri"]
                    
                    missing_fields = [field for field in required_fields if not credentials.get(field)]
                    if missing_fields:
                        st.error(f"❌ Eksik alanlar: {', '.join(missing_fields)}")
                    else:
                        st.success("✅ Tüm gerekli alanlar mevcut")
                        
                    # Check private key format
                    private_key = credentials.get("private_key", "")
                    if private_key:
                        if private_key.startswith("-----BEGIN PRIVATE KEY-----"):
                            st.success("✅ Private key formatı doğru")
                        else:
                            st.error("❌ Private key formatı hatalı")
                    else:
                        st.error("❌ Private key bulunamadı")
                        
                else:
                    st.error("❌ Service account secrets bulunamadı")
                
                st.info("🔧 **Olası çözümler:**")
                st.write("1. Streamlit Cloud app'ı restart edin")
                st.write("2. Google Cloud Console'da API'lerin aktif olduğunu kontrol edin")
                st.write("3. Service Account'un Sheet'e erişim izni olduğunu kontrol edin")
                st.write("4. Private key formatının doğru olduğunu kontrol edin")
                
            sheet_id = st.secrets.get("GOOGLE_SHEET_ID")
            if sheet_id:
                st.success(f"✅ Sheet ID: {sheet_id[:10]}...")
                st.code(f"Sheet URL: https://docs.google.com/spreadsheets/d/{sheet_id}")
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
                    
                # Show credential creation status
                if self.gsheet_client is None:
                    st.warning("⚠️ Client oluşturma süreci başarısız - Console output'u kontrol edin")
        
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
            
            # List all worksheets for debugging
            worksheets = spreadsheet.worksheets()
            worksheet_names = [ws.title for ws in worksheets]
            st.info(f"🔧 Debug: Mevcut worksheet'ler: {worksheet_names}")
            
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
                
            # Alternative: Use first worksheet if Feedback doesn't exist
            if not worksheet:
                worksheet = worksheets[0]
                st.warning(f"🔧 Debug: İlk worksheet kullanılıyor: {worksheet.title}")
            
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
