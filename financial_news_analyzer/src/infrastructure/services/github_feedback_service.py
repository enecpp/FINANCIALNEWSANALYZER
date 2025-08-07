import requests
import json
from datetime import datetime
import streamlit as st # type: ignore


class GitHubFeedbackService:
    """
    Alternative feedback service using GitHub Issues API.
    More reliable than Google Sheets for Streamlit Cloud.
    """
    
    def __init__(self):
        self.github_token = st.secrets.get("GITHUB_TOKEN", "")
        self.repo_owner = st.secrets.get("GITHUB_REPO_OWNER", "enecpp")
        self.repo_name = st.secrets.get("GITHUB_REPO_NAME", "FINANCIALNEWSANALYZER")
        self.api_base = "https://api.github.com"
        
    def is_configured(self) -> bool:
        """Check if GitHub integration is properly configured."""
        return bool(self.github_token and self.repo_owner and self.repo_name)
    
    def save_feedback(self, name: str, email: str, message: str) -> bool:
        """
        Save feedback as a GitHub Issue.
        
        Args:
            name: User's name
            email: User's email  
            message: Feedback message
            
        Returns:
            bool: True if successfully saved
        """
        if not self.is_configured():
            return False
            
        try:
            # Create issue title and body
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            title = f"💬 Feedback from {name} - {timestamp}"
            
            body = f"""
## 📝 User Feedback

**👤 Name:** {name}  
**📧 Email:** {email}  
**🕒 Timestamp:** {timestamp}  

---

### 💬 Message:
{message}

---

*This feedback was automatically created via the Financial News Analyzer contact form.*
            """.strip()
            
            # Create GitHub issue
            url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/issues"
            
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            }
            
            data = {
                "title": title,
                "body": body,
                "labels": ["feedback", "contact-form"]
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 201:
                issue_data = response.json()
                issue_number = issue_data.get("number")
                st.success(f"✅ Feedback GitHub Issue #{issue_number} olarak kaydedildi!")
                return True
            else:
                st.error(f"❌ GitHub API Error: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Network error: {str(e)}")
            return False
        except Exception as e:
            st.error(f"❌ GitHub feedback error: {str(e)}")
            return False
            
    def test_connection(self) -> bool:
        """Test GitHub API connection."""
        if not self.is_configured():
            return False
            
        try:
            url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
            
        except Exception:
            return False
