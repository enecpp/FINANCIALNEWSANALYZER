import streamlit as st  # type: ignore
import sys
import os
from datetime import datetime

# src klasörünü import yoluna ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from infrastructure.services.feedback_service import FeedbackService

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
with st.form("contact_form"):
    name = st.text_input("Name", placeholder="Your name")
    email = st.text_input("Email", placeholder="you@example.com")
    message = st.text_area("Message", placeholder="Type your message here...", height=150)
    submitted = st.form_submit_button("Send Message")
    if submitted:
        svc = FeedbackService(st.secrets)
        svc.save(name, email, message)
        st.success("Thank you for your message! We'll get back to you soon.")

# İletişim e-posta kartı
st.markdown("""
<div class="metric-card">
  <strong>Email:</strong> <a href="mailto:enesor8@gmail.com">enesor8@gmail.com</a>
</div>
""", unsafe_allow_html=True)
