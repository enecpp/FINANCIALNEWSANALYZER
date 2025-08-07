import streamlit as st  # type: ignore
import sys
import os
from datetime import datetime

# src klasörünü import yoluna ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Feedback service import'u try-except ile güvenli hale getir
try:
    from infrastructure.services.feedback_service import FeedbackService ##type: ignore
    FEEDBACK_SERVICE_AVAILABLE = True
except ImportError:
    FEEDBACK_SERVICE_AVAILABLE = False

# Sayfa ayarları
st.set_page_config(
    page_title="✉️ Contact Us",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_custom_css():
    st.markdown("""
    <style>
      :root {
        --primary-bg: #1a1a1a;
        --gradient-1: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        --text-primary: #ffffff;
      }
      .stApp { background: var(--primary-bg) !important; color: var(--text-primary); }
      .main .block-container {
        background: var(--primary-bg) !important;
        padding: 2rem; border-radius: 15px;
        animation: fadeInUp 1s ease-out;
      }
      @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
      }
      .stButton > button {
        background: var(--gradient-1);
        color: #fff; border-radius: 8px;
        padding: 12px 30px; transition: all 0.3s ease;
      }
      .stButton > button:hover { transform: scale(1.02); }
      .metric-card {
        background: var(--gradient-1); padding: 15px;
        border-radius: 12px; margin-top: 1rem;
        color: #fff;
      }
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# Başlık bölümü
st.markdown('''
<div style="background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%);
            color: #ffffff; padding: 2.5rem; border-radius: 12px;
            text-align: center; margin-bottom: 2rem;">
  <h1 style="margin:0; font-size:3rem; font-weight:700;">✉️ Contact Us</h1>
  <h3 style="font-weight:300; font-size:1.2rem; color:#bdc3c7;">
    Get in touch with our team for inquiries, feedback, or support
  </h3>
</div>
''', unsafe_allow_html=True)

# İletişim formu
if 'form_submitted' in st.session_state and st.session_state.form_submitted:
    # Reset form state
    st.session_state.form_submitted = False
    
with st.form("contact_form", clear_on_submit=True):
    st.markdown("### 📝 Bize Ulaşın")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👤 İsim", placeholder="Adınız ve soyadınız", key="contact_name")
        
    with col2:
        email = st.text_input("📧 E-posta", placeholder="ornek@email.com", key="contact_email")
    
    message = st.text_area(
        "💬 Mesaj", 
        placeholder="Mesajınızı buraya yazın...", 
        height=150,
        help="Görüşleriniz, önerileriniz veya sorularınız için...",
        key="contact_message"
    )
    
    submitted = st.form_submit_button("📨 Mesaj Gönder", use_container_width=True)
    
    if submitted:
        if name.strip() and email.strip() and message.strip():
            if FEEDBACK_SERVICE_AVAILABLE:
                try:
                    with st.spinner("Mesajınız gönderiliyor..."):
                        svc = FeedbackService(st.secrets)
                        success = svc.save(name.strip(), email.strip(), message.strip())
                        
                        if success:
                            # Clear form by rerunning
                            st.balloons()
                            st.success("✅ Mesajınız başarıyla gönderildi!")
                            # Form temizlemek için session state kullan
                            if 'form_submitted' not in st.session_state:
                                st.session_state.form_submitted = True
                                st.rerun()
                except Exception as e:
                    st.error(f"❌ Mesaj gönderilirken hata oluştu: {str(e)}")
            else:
                st.error("❌ Feedback servisi şu anda kullanılamıyor. Lütfen doğrudan email gönderin.")
        else:
            st.error("⚠️ Lütfen tüm alanları doldurun!")

# İletişim e-posta kartı
st.markdown("""
<div class="metric-card">
  <strong>📧 Email:</strong> <a href="mailto:enesor8@gmail.com" style="color: #fff; text-decoration: none;">enesor8@gmail.com</a>
</div>
""", unsafe_allow_html=True)

# Debug bilgileri (development aşamasında)
with st.expander("🔧 Debug Bilgileri", expanded=False):
    if not FEEDBACK_SERVICE_AVAILABLE:
        st.warning("ℹ️ Feedback servisi şu anda yapılandırılmıyor. Mesajlar doğrudan email ile gönderilebilir.")
    else:
        try:
            # Secrets kontrolü
            if hasattr(st, 'secrets'):
                st.info("✅ Streamlit secrets yapılandırılmış")
                
                # Google Sheet ID kontrolü
                if "GOOGLE_SHEET_ID" in st.secrets:
                    sheet_id = st.secrets["GOOGLE_SHEET_ID"]
                    st.success(f"✅ Google Sheet ID: {sheet_id[:10]}...")
                else:
                    st.error("❌ Google Sheet ID eksik!")
                
                # Service Account kontrolü
                if "gcp_service_account" in st.secrets:
                    service_account = st.secrets["gcp_service_account"]
                    project_id = service_account.get("project_id", "")
                    client_email = service_account.get("client_email", "")
                    
                    if project_id and project_id != "your-actual-project-id":
                        st.success("✅ Google Cloud Service Account - Project ID yapılandırılmış")
                    else:
                        st.warning("⚠️ Google Cloud Service Account - Project ID placeholder değerde")
                        st.info("💡 **Çözüm:** Google Cloud Console'dan Service Account oluşturun ve gerçek project_id'yi girin")
                    
                    if client_email and "@" in client_email and "your-project.iam.gserviceaccount.com" not in client_email:
                        st.success("✅ Google Cloud Service Account - Client Email yapılandırılmış")
                    else:
                        st.warning("⚠️ Google Cloud Service Account - Client Email placeholder değerde")
                        st.info("💡 **Çözüm:** Service Account JSON'ından client_email değerini kopyalayın")
                        
                    if service_account.get("private_key") and "BEGIN PRIVATE KEY" in service_account.get("private_key", ""):
                        if "your-actual-private-key" not in service_account.get("private_key", ""):
                            st.success("✅ Google Cloud Service Account - Private Key yapılandırılmış")
                        else:
                            st.warning("⚠️ Google Cloud Service Account - Private Key placeholder değerde")
                    else:
                        st.error("❌ Google Cloud Service Account - Private Key eksik!")
                else:
                    st.error("❌ Google Cloud Service Account bilgileri eksik!")
                    
                # Test FeedbackService initialization
                st.write("**🔧 Service Test:**")
                try:
                    test_service = FeedbackService(st.secrets)
                    if test_service.gsheet_client:
                        st.success("✅ Google Sheets client başarıyla oluşturuldu")
                    else:
                        st.error("❌ Google Sheets client oluşturulamadı")
                        st.info("📋 **Console Logs kontrolü için Streamlit Cloud logs'una bakın**")
                except Exception as service_error:
                    st.error(f"❌ Service initialization error: {str(service_error)}")
                    
                # CSV fallback bilgisi
                st.info("📁 CSV Fallback: Aktif (Google Sheets çalışmazsa mesajlar CSV dosyasına kaydedilir)")
                
                # Console logs access
                st.info("📊 **Console Logs Erişimi:**")
                st.code("""
1. Streamlit Cloud dashboard'a gidin
2. App'ınızı seçin  
3. "Logs" sekmesine tıklayın
4. "DEBUG: " ile başlayan mesajları arayın
                """)
                
                # Placeholder uyarısı
                if ("your-actual-project-id" in str(st.secrets.get("gcp_service_account", {})) or 
                    "your-project" in str(st.secrets.get("gcp_service_account", {}).get("client_email", ""))):
                    st.warning("⚠️ **Google Sheets için gerçek Service Account bilgileri gerekli**")
                    st.info("""
                    **Çözüm:**
                    1. Google Cloud Console'da Service Account oluşturun
                    2. JSON key dosyasını indirin  
                    3. Streamlit Cloud secrets'ına gerçek bilgileri kopyalayın
                    4. App'ı reboot edin
                    
                    **Şu anda:** Mesajlar CSV dosyasına kaydediliyor ✅
                    """)
                else:
                    st.success("🔑 Service Account bilgileri placeholder değil - Google Sheets bağlantısı hazır")
                
            else:
                st.error("❌ Streamlit secrets yapılandırılmamış!")
        except Exception as e:
            st.error(f"❌ Secrets kontrolü sırasında hata: {str(e)}")

# Manual fallback test button
with st.expander("🧪 Manual Test", expanded=False):
    if st.button("🔄 Service Test"):
        if FEEDBACK_SERVICE_AVAILABLE:
            try:
                with st.spinner("Service test ediliyor..."):
                    test_service = FeedbackService(st.secrets)
                    
                    if test_service.gsheet_client:
                        st.success("✅ Google Sheets client çalışıyor!")
                        
                        # Test actual connection
                        try:
                            sheet_id = st.secrets.get("GOOGLE_SHEET_ID")
                            if sheet_id:
                                test_sheet = test_service.gsheet_client.open_by_key(sheet_id)
                                st.success(f"✅ Sheet erişimi başarılı: {test_sheet.title}")
                            else:
                                st.error("❌ Sheet ID bulunamadı")
                        except Exception as sheet_error:
                            st.error(f"❌ Sheet erişim hatası: {str(sheet_error)}")
                    else:
                        st.error("❌ Google Sheets client oluşturulamadı")
                        st.info("📋 Console logs'da 'DEBUG:' mesajlarını kontrol edin")
                        
                        # Force CSV test
                        st.info("🔄 CSV fallback test ediliyor...")
                        csv_success = test_service._save_to_csv({
                            'timestamp': datetime.utcnow().isoformat(),
                            'name': 'Test User',
                            'email': 'test@example.com',
                            'message': 'Test message from manual test'
                        })
                        
                        if csv_success:
                            st.success("✅ CSV fallback çalışıyor!")
                        else:
                            st.error("❌ CSV fallback da başarısız!")
                            
            except Exception as test_error:
                st.error(f"❌ Service test hatası: {str(test_error)}")
        else:
            st.error("❌ Feedback service mevcut değil")

# Form başarı durumu
if 'form_submitted' in st.session_state and st.session_state.form_submitted:
    st.success("✅ Form başarıyla temizlendi!")
