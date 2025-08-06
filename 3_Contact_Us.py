"""
Contact Us Page
Get in touch with our team for inquiries, feedback, or support
"""

import streamlit as st  # type: ignore
import os
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

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
    button[title="View fullscreen"] { visibility: hidden; }
    button[data-testid="collapsedControl"] {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border-radius: 8px !important;
    }
    button[data-testid="collapsedControl"]:hover {
        transform: scale(1.1) rotate(5deg) !important;
        background-color: rgba(0, 212, 170, 0.1) !important;
        box-shadow: 0 4px 12px rgba(0, 212, 170, 0.3) !important;
    }
    button[data-testid="collapsedControl"]:active {
        transform: scale(0.95) !important;
        transition: all 0.1s ease-in-out !important;
    }
    /* Modern animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 212, 170, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 212, 170, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 212, 170, 0); }
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(0, 212, 170, 0.3); }
        50% { box-shadow: 0 0 20px rgba(0, 212, 170, 0.8), 0 0 30px rgba(0, 212, 170, 0.4); }
    }
    /* App background with animation */
    .stApp {
        background-color: var(--primary-bg) !important;
        color: var(--text-primary);
        animation: fadeInUp 0.8s ease-out;
    }
    .main .block-container {
        background: var(--primary-bg) !important;
        color: var(--text-primary);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 1rem;
        animation: fadeInUp 1s ease-out;
    }
    /* Custom cards with animations */
    .metric-card {
        background: var(--gradient-1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin: 10px 0;
        color: var(--text-primary);
        animation: slideInLeft 0.6s ease-out;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 212, 170, 0.2);
        animation: glow 2s infinite;
    }
    /* Animated gradient text */
    .gradient-text {
        background: var(--gradient-2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 30px;
        background-size: 200% 200%;
        animation: gradient-shift 3s ease-in-out infinite, slideInRight 1s ease-out;
    }
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    /* Custom buttons with enhanced smooth transitions */
    .stButton > button {
        background: var(--gradient-1);
        color: white;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 212, 170, 0.3);
        background: var(--tertiary-bg);
    }
    .stButton > button:active {
        transform: translateY(-1px) scale(1.01);
        transition: all 0.1s ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the custom theme CSS
load_custom_css()

# Page header
st.markdown('''
<div style="background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%); 
            color: #ffffff; padding: 2.5rem; border-radius: 12px; text-align: center; 
            margin-bottom: 2rem; box-shadow: 0 6px 20px rgba(0,0,0,0.4); 
            border: 1px solid #3a3a3a;">
    <h1 style="margin: 0; font-size: 3rem; font-weight: 700; color: #ffffff;">
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
