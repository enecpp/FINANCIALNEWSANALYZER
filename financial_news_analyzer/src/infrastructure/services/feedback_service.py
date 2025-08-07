import os
import csv
from datetime import datetime

import streamlit as st # type: ignore

# Import GitHub feedback service
try:
    from .github_feedback_service import GitHubFeedbackService
    GITHUB_FEEDBACK_AVAILABLE = True
except ImportError:
    GITHUB_FEEDBACK_AVAILABLE = False


class FeedbackService:
    """
    Service for saving user feedback with GitHub Issues and CSV fallback.
    Priority: GitHub Issues -> CSV
    """
    def __init__(self, secrets: dict):
        self.secrets = secrets
        self.github_service = None
        
        # Initialize GitHub service (preferred)
        if GITHUB_FEEDBACK_AVAILABLE:
            self.github_service = GitHubFeedbackService()
        
        # Prepare local CSV path as fallback
        self.csv_dir = os.path.join(os.getcwd(), 'data')
        os.makedirs(self.csv_dir, exist_ok=True)
        self.csv_file = os.path.join(self.csv_dir, 'feedback.csv')

    def save(self, name: str, email: str, message: str) -> bool:
        """
        Save feedback with GitHub Issues and CSV fallback.
        Priority: GitHub Issues -> CSV
        
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
            st.write("**📊 Mevcut Backend'ler:**")
            
            # GitHub Status
            if self.github_service and self.github_service.is_configured():
                if self.github_service.test_connection():
                    st.success("✅ GitHub Issues API hazır")
                else:
                    st.warning("⚠️ GitHub API bağlantı sorunu")
            elif GITHUB_FEEDBACK_AVAILABLE:
                st.warning("⚠️ GitHub Issues - Konfigürasyon eksik")
                st.info("💡 GITHUB_TOKEN gerekli")
            else:
                st.info("ℹ️ GitHub Issues servisi mevcut değil")
                
            # CSV Status
            st.success("✅ CSV Fallback hazır")
                
        # Try GitHub Issues first (most reliable)
        if self.github_service and self.github_service.is_configured():
            if self.github_service.save_feedback(name, email, message):
                st.success("✅ Mesajınız GitHub Issues'a başarıyla kaydedildi!")
                return True
        
        # Use CSV as fallback
        if self._save_to_csv(data):
            st.success("✅ Mesajınız başarıyla kaydedildi!")
            st.info("📁 Mesajlar CSV dosyasında güvenle saklanıyor.")
            return True
        
        st.error("❌ Mesaj kaydedilemedi. Lütfen daha sonra tekrar deneyin.")
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
