import streamlit as st  # type: ignore
import sys
import os
# Projenin src klasörünü import yoluna ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from infrastructure.services.feedback_service import FeedbackService
# Sayfa konfigürasyonu
st.set_page_config(
    page_title="✉️ Contact Us",
    layout="wide",
    initial_sidebar_state="collapsed"
)
def load_custom_css():
    """Uygulamaya özel tema CSS'ini yükler"""
    st.markdown("""
    .stApp { background: var(--primary-bg) !important; color: var(--text-primary); }
    .main .block-container {
        background: var(--primary-bg) !important;
    .stButton > button:hover { transform: scale(1.02); }
    .metric-card {
        background: var(--gradient-1);
    </style>
    """, unsafe_allow_html=True)

load_custom_css()
# Başlık bölümü
st.markdown('''
<div style="background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%);
    ✉️ Contact Us
  </h1>
  <h3 style="font-weight:300; font-size:1.2rem; color:#bdc3c7;">
    Get in touch with our team for inquiries, feedback, or support
  </h3>
</div>
with st.form("contact_form"):
    name = st.text_input("Name", placeholder="Your name")
    email = st.text_input("Email", placeholder="you@example.com")
    message = st.text_area("Message", placeholder="Type your message here...", height=150)
    submitted = st.form_submit_button("Send Message")
    if submitted:
        svc = FeedbackService(st.secrets)
        svc.save(name, email, message)
        st.success("Thank you for your message! We'll get back to you soon.")
""", unsafe_allow_html=True)
""", unsafe_allow_html=True)
""", unsafe_allow_html=True)

import streamlit as st  # type: ignore
import sys
import os
# Ensure src folder is on Python path for infrastructure imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from datetime import datetime
# Onion architecture service for feedback persistence
from infrastructure.services.feedback_service import FeedbackService

# Page configuration
st.set_page_config(
    page_title="✉️ Contact Us",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_custom_css():
    """Load custom CSS for consistent styling"""
    st.markdown("""
    <style>
    /* Main theme colors - matching Start.py */
    :root {
        --primary-bg: #1a1a1a;
        --secondary-bg: #2c3e50;
        --tertiary-bg: #34495e;
        --accent-color: #00D4AA;
        --text-primary: #ffffff;
        --text-secondary: #bdc3c7;
        --border-color: #3a3a3a;
        --gradient-1: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        --gradient-2: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    /* Hide some Streamlit default elements but keep hamburger menu */
    footer {visibility: hidden;}
        ✉️ Contact Us
    </h1>
    <h3 style="font-weight: 300; font-size: 1.5rem; color: #bdc3c7; margin: 1rem 0;">
        Get in touch with our team for inquiries, feedback, or support
    </h3>
</div>
''', unsafe_allow_html=True)

with st.form("contact_form"):
    name = st.text_input("Name", placeholder="Your name")
    email = st.text_input("Email", placeholder="your.email@example.com")
    message = st.text_area("Message", placeholder="Type your message here...", height=150)
    submitted = st.form_submit_button("Send Message")
    if submitted:
        # Append feedback to CSV file
        feedback_dir = os.path.join(os.getcwd(), 'data')
        os.makedirs(feedback_dir, exist_ok=True)
        feedback_file = os.path.join(feedback_dir, 'feedback.csv')
        file_exists = os.path.exists(feedback_file)
        with open(feedback_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Timestamp', 'Name', 'Email', 'Message'])
            writer.writerow([datetime.now().isoformat(), name, email, message])
        st.success("Thank you for your message! We'll get back to you soon.")
        # Send feedback via email
        try:
            smtp_host = os.getenv('SMTP_HOST', 'smtp.example.com')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            smtp_user = os.getenv('SMTP_USER')
            smtp_pass = os.getenv('SMTP_PASS')
            recipient = os.getenv('FEEDBACK_RECIPIENT', smtp_user)
            subject = f"New Feedback from {name}"
            body = f"Time: {datetime.now().isoformat()}\nName: {name}\nEmail: {email}\nMessage:\n{message}"
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = smtp_user
            msg['To'] = recipient
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            st.error(f"Could not send feedback email: {e}")

st.markdown("""
<div class="metric-card">
  <strong>Email:</strong> <a href="mailto:enesor8@gmail.com">enesor8@gmail.com, </a><br>

</div>
""", unsafe_allow_html=True)
