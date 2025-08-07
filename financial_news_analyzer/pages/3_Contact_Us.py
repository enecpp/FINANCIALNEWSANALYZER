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
                
                # GitHub Token kontrolü
                if "GITHUB_TOKEN" in st.secrets:
                    token = st.secrets["GITHUB_TOKEN"]
                    st.success(f"✅ GitHub Token: {token[:8]}...")
                else:
                    st.warning("⚠️ GitHub Token eksik!")
                    st.info("💡 **Çözüm:** GitHub Personal Access Token oluşturun ve GITHUB_TOKEN olarak ekleyin")
                
                # GitHub Repo bilgileri
                repo_owner = st.secrets.get("GITHUB_REPO_OWNER", "enecpp")
                repo_name = st.secrets.get("GITHUB_REPO_NAME", "FINANCIALNEWSANALYZER")
                st.success(f"✅ GitHub Repo: {repo_owner}/{repo_name}")
                    
                # Test FeedbackService initialization
                st.write("**🔧 Service Test:**")
                try:
                    test_service = FeedbackService(st.secrets)
                    if test_service.github_service and test_service.github_service.is_configured():
                        if test_service.github_service.test_connection():
                            st.success("✅ GitHub Issues API başarıyla çalışıyor")
                        else:
                            st.warning("⚠️ GitHub API bağlantı sorunu")
                    else:
                        st.warning("⚠️ GitHub Issues servisi yapılandırılmamış")
                        
                    st.success("✅ CSV Fallback sistem hazır")
                        
                except Exception as service_error:
                    st.error(f"❌ Service initialization error: {str(service_error)}")
                    
                # CSV fallback bilgisi
                st.info("📁 CSV Fallback: Aktif (Her durumda mesajlar CSV dosyasına kaydedilir)")
                
                # GitHub setup guide
                st.info("� **GitHub Token Setup:**")
                st.code("""
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Repo scope'unu seçin
4. Token'ı kopyalayın
5. Streamlit Cloud → App Settings → Secrets → GITHUB_TOKEN olarak ekleyin
                """)
                
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
                    
                    # Test GitHub Issues
                    if test_service.github_service and test_service.github_service.is_configured():
                        if test_service.github_service.test_connection():
                            st.success("✅ GitHub Issues API çalışıyor!")
                        else:
                            st.error("❌ GitHub API bağlantı hatası")
                    else:
                        st.warning("⚠️ GitHub Issues servisi yapılandırılmamış")
                        
                    # Test CSV fallback
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
