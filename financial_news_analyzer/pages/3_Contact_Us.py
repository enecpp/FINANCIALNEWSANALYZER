

import streamlit as st ##type: ignore 
from datetime import datetime
import urllib.parse

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
    /* Main theme colors - matching other pages */
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
        --contact-gradient: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
    }
    
    /* Hide some Streamlit default elements but keep hamburger menu */
    footer {visibility: hidden;}
    
    /* Enhanced hamburger menu animation */
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
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
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
    .contact-card {
        background: var(--gradient-1);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin: 15px 0;
        color: var(--text-primary);
        animation: slideInLeft 0.6s ease-out;
    }
    
    .contact-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 212, 170, 0.2);
        animation: glow 2s infinite;
    }
    
    .info-card {
        background: var(--contact-gradient);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin: 10px 0;
        color: var(--text-primary);
        animation: slideInRight 0.6s ease-out;
    }
    
    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(255, 107, 107, 0.3);
    }
    
    /* Contact method cards */
    .contact-method {
        background: var(--gradient-2);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
        margin: 10px 0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .contact-method:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .contact-method a {
        color: var(--text-primary);
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .contact-method a:hover {
        color: var(--accent-color);
    }
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: var(--secondary-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 1px var(--accent-color) !important;
    }
    
    /* Custom buttons */
    .stButton > button {
        background: var(--gradient-1);
        color: white;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        width: 100%;
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
    
    /* Success/error message styling */
    .stSuccess {
        animation: slideInLeft 0.5s ease-out;
    }
    
    .stError {
        animation: slideInRight 0.5s ease-out;
    }
    
    /* Social links */
    .social-links {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 20px 0;
    }
    
    .social-link {
        display: inline-block;
        padding: 12px;
        background: var(--gradient-3);
        border-radius: 50%;
        transition: all 0.3s ease;
        text-decoration: none;
        color: white;
        font-size: 1.5rem;
    }
    
    .social-link:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
    }
    
    /* Office hours card */
    .office-hours {
        background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 15px 0;
        animation: pulse 3s infinite;
    }
    
    /* FAQ section */
    .faq-item {
        background: var(--gradient-1);
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        border-left: 4px solid var(--accent-color);
        transition: all 0.3s ease;
    }
    
    .faq-item:hover {
        transform: translateX(10px);
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.2);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .contact-method {
            margin: 5px 0;
            padding: 15px;
        }
        
        .social-links {
            gap: 15px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main function for Contact Us page"""
    load_custom_css()
    
    # Header - matching other pages design
    st.markdown("""
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
        <p style="color: #95a5a6; margin: 0.5rem 0;">
            We're here to help you with your financial analysis needs
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact methods section
    st.subheader("📞 Contact Methods")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="contact-method">
            <h3>📧 Email</h3>
            <a href="mailto:enesor8@gmail.com">enesor8@gmail.com</a>
            <p style="margin-top: 10px; font-size: 0.9rem; color: #bdc3c7;">
                Response within 24 hours
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="contact-method">
            <h3>💬 Support</h3>
            <p style="color: #00D4AA; font-weight: 600;">Live Chat</p>
            <p style="margin-top: 10px; font-size: 0.9rem; color: #bdc3c7;">
                Available 9 AM - 6 PM
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="contact-method">
            <h3>🌐 Social</h3>
            <div class="social-links">
                <a href="#" class="social-link" title="LinkedIn">💼</a>
                <a href="#" class="social-link" title="Twitter">🐦</a>
                <a href="#" class="social-link" title="GitHub">💻</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main contact form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="contact-card">
            <h3 style="margin-top: 0;">📝 Send us a Message</h3>
            <p style="color: #bdc3c7; margin-bottom: 20px;">
                Fill out the form below and we'll get back to you as soon as possible.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Contact Form with Streamlit components
        with st.form("contact_form", clear_on_submit=True):
            # Form styling container
            st.markdown("""
            <div style="background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); 
                        padding: 30px; border-radius: 15px; border: 1px solid #3a3a3a; 
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); margin: 20px 0;">
            """, unsafe_allow_html=True)
            
            # Form fields
            col_name, col_email = st.columns(2)
            with col_name:
                name = st.text_input("👤 Full Name *", placeholder="Enter your full name", key="name")
            with col_email:
                email = st.text_input("📧 Email Address *", placeholder="your.email@example.com", key="email")
            
            col_subject, col_priority = st.columns(2)
            with col_subject:
                subject = st.selectbox("📋 Subject", [
                    "General Inquiry", "Technical Support", "Feature Request", 
                    "Bug Report", "Partnership", "Investment Advice", "API Access", "Other"
                ], key="subject")
            with col_priority:
                priority = st.selectbox("🚨 Priority", ["Low", "Medium", "High", "Urgent"], index=1, key="priority")
            
            message = st.text_area("💬 Message *", placeholder="Please describe your inquiry in detail...", 
                                 height=150, key="message")
            
            st.markdown("### 📊 Additional Options")
            col_opt1, col_opt2, col_opt3 = st.columns(3)
            with col_opt1:
                newsletter = st.checkbox("📰 Newsletter", help="Subscribe to market updates")
            with col_opt2:
                updates = st.checkbox("� Product Updates", help="Receive new features notifications")
            with col_opt3:
                callback = st.checkbox("📞 Request Callback", help="For urgent matters")
            
            # Submit button
            submitted = st.form_submit_button("📨 Send Message", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Handle form submission
            if submitted:
                if name and email and message:
                    # Create FormSubmit URL with parameters
                    import urllib.parse
                    
                    # Prepare form data
                    form_data = {
                        "name": name,
                        "email": email,
                        "subject": subject,
                        "priority": priority,
                        "message": message,
                        "newsletter": "Yes" if newsletter else "No",
                        "updates": "Yes" if updates else "No", 
                        "callback": "Yes" if callback else "No",
                        "_subject": f"📧 New Contact - {subject} ({priority} Priority)",
                        "_captcha": "false",
                        "_template": "table"
                    }
                    
                    # Create FormSubmit URL
                    base_url = "https://formsubmit.co/enesor8@gmail.com"
                    query_string = urllib.parse.urlencode(form_data)
                    formsubmit_url = f"{base_url}?{query_string}"
                    
                    # Success message and redirect
                    st.success("✅ Thank you! Your message is being sent...")
                    st.markdown(f"""
                    <script>
                        window.open('{formsubmit_url}', '_blank');
                    </script>
                    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #27AE60 0%, #2ECC71 100%); 
                                border-radius: 10px; color: white; margin: 20px 0;">
                        <h3>📧 Message Sent Successfully!</h3>
                        <p>We'll get back to you within 24 hours.</p>
                        <p><strong>Details:</strong> {subject} | Priority: {priority}</p>
                        <a href="{formsubmit_url}" target="_blank" style="color: white; text-decoration: underline;">
                            Click here if the email form doesn't open automatically
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Alternative: Direct FormSubmit link
                    st.markdown(f"""
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="{formsubmit_url}" target="_blank" 
                           style="background: linear-gradient(135deg, #00D4AA 0%, #007B5E 100%); 
                                  color: white; padding: 15px 30px; border-radius: 8px; 
                                  text-decoration: none; font-weight: 600; display: inline-block;
                                  box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);">
                            📨 Send via FormSubmit
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ Please fill in all required fields (Name, Email, Message)")
    
    with col2:
        # Contact information card
        st.markdown("""
        <div class="info-card">
            <h3 style="margin-top: 0;">📍 Contact Information</h3>
            <div style="margin: 15px 0;">
                <strong>📧 Email:</strong><br>
                <a href="mailto:enesor8@gmail.com" style="color: white;">enesor8@gmail.com</a>
            </div>
            <div style="margin: 15px 0;">
                <strong>🌐 Website:</strong><br>
                <span style="color: #00D4AA;">Financial News Analyzer</span>
            </div>
            <div style="margin: 15px 0;">
                <strong>💼 Services:</strong><br>
                • Financial Analysis<br>
                • Market Data<br>
                • Investment Insights<br>
                • Technical Support
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Office hours
        st.markdown("""
        <div class="office-hours">
            <h4 style="margin-top: 0;">🕒 Response Hours</h4>
            <p><strong>Monday - Friday:</strong> 9:00 AM - 6:00 PM</p>
            <p><strong>Saturday:</strong> 10:00 AM - 4:00 PM</p>
            <p><strong>Sunday:</strong> Closed</p>
            <p style="font-size: 0.9rem; margin-top: 15px;">
                <em>Emergency support available 24/7 for critical issues</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick tips
        st.markdown("""
        <div class="contact-card">
            <h4 style="margin-top: 0;">💡 Quick Tips</h4>
            <ul style="color: #bdc3c7; padding-left: 20px;">
                <li>Include specific details about your issue</li>
                <li>Mention your platform/browser if reporting bugs</li>
                <li>Check our FAQ section first</li>
                <li>Use the correct priority level</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # FAQ Section
    st.markdown("---")
    st.subheader("❓ Frequently Asked Questions")
    
    faq_col1, faq_col2 = st.columns(2)
    
    with faq_col1:
        with st.expander("🔒 Is my data secure?", expanded=False):
            st.write("""
            Yes, we take data security seriously. All communications are encrypted, 
            and we follow industry best practices for data protection.
            """)
        
        with st.expander("📊 How do I access premium features?", expanded=False):
            st.write("""
            Premium features are currently in development. Contact us to be notified 
            when they become available or to discuss enterprise solutions.
            """)
        
        with st.expander("🛠️ Technical support hours?", expanded=False):
            st.write("""
            Technical support is available Monday-Friday 9 AM - 6 PM. 
            Critical issues receive 24/7 support.
            """)
    
    with faq_col2:
        with st.expander("💰 Is there a cost for using the platform?", expanded=False):
            st.write("""
            The basic financial analysis tools are free. Premium features and 
            enterprise solutions are available on request.
            """)
        
        with st.expander("📱 Mobile app availability?", expanded=False):
            st.write("""
            We're currently focused on the web platform. Mobile optimization 
            is on our roadmap for future releases.
            """)
        
        with st.expander("🔄 How often is data updated?", expanded=False):
            st.write("""
            Market data is updated in real-time during trading hours. 
            News analysis is updated continuously throughout the day.
            """)
    
    # Footer with additional links
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="color: #95a5a6;">
            <strong>Need immediate help?</strong> 
            <a href="mailto:enesor8@gmail.com" style="color: #00D4AA;">Send us an email</a> 
            and we'll respond as quickly as possible.
        </p>
        <p style="color: #7f8c8d; font-size: 0.9rem;">
            Financial News Analyzer © 2024 - Professional Financial Analysis Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
