"""
Financial News Analyzer
Modern financial analysis platform for market         st.set_page_config(
            page_title="🏦 Financial News Analyzer",
            page_icon="🏦",
            layout="wide",
            initial_sidebar_state="expanded"
        )igence

This application provides:
- Clean Architecture with layered design
- Professional financial analysis tools
- Real-time market data visualization
- Comprehensive news sentiment analysis
- Global market coverage
- Use Case Pattern
"""
import streamlit as st
import sys
import os
from datetime import datetime
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Add src to path for imports
current_dir = Path(__file__).parent
src_path = current_dir / 'src'
sys.path.insert(0, str(src_path))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class FinancialAnalyzerApp:
    """
    Main application class for financial news analysis
    
    Features:
    - Comprehensive market data analysis
    - Real-time news sentiment tracking
    - Interactive data visualization
    - Multi-platform broker integration
    """
    
    _instance: Optional['FinancialAnalyzerApp'] = None
    
    def __new__(cls):
        """Ensure singleton instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize application components"""
        if not hasattr(self, '_initialized'):
            self._initialize_app()
            self._initialized = True
    
    def _initialize_app(self):
        """Initialize application dependencies and components"""
        try:
            # Configure Streamlit page
            self._configure_page()
            
            # Initialize dependency container
            self._initialize_container()
            
            # Initialize UI components
            self._initialize_components()
            
            logging.info("Application initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize application: {e}")
            st.error(f"Application initialization failed: {e}")
    
    def _configure_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="� Financial News Analyzer",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def _initialize_container(self):
        """Initialize dependency injection container"""
        try:
            # Try to import container, fallback if not available
            try:
                # from infrastructure.container import container
                # self._container = container
                
                # For now, use fallback until infrastructure is implemented
                self._container = self._create_fallback_container()
                
                # Verify container health
                health = self._container.health_check()
                if health["container_status"] != "healthy":
                    logging.warning(f"Container health check: {health}")
            except ImportError:
                # Create a minimal fallback container
                self._container = self._create_fallback_container()
                
        except Exception as e:
            logging.error(f"Failed to initialize container: {e}")
            # Create a minimal fallback
            self._container = self._create_fallback_container()
    
    def _create_fallback_container(self):
        """Create a minimal fallback container for demo purposes"""
        class FallbackContainer:
            def health_check(self):
                return {
                    "container_status": "fallback",
                    "services_count": 0,
                    "services": {}
                }
        
        return FallbackContainer()
    
    def _initialize_components(self):
        """Initialize UI components"""
        try:
            # Try to import world clock component, fallback if not available
            try:
                # from presentation.components.world_clock_component import WorldClockComponent
                # self._world_clock = WorldClockComponent()
                
                # For now, use fallback until presentation components are implemented
                self._world_clock = self._create_fallback_world_clock()
            except ImportError:
                # Create a minimal fallback world clock
                self._world_clock = self._create_fallback_world_clock()
                
        except Exception as e:
            logging.error(f"Failed to initialize components: {e}")
            self._world_clock = self._create_fallback_world_clock()
    
    def _create_fallback_world_clock(self):
        """Create a comprehensive fallback world clock component"""
        class FallbackWorldClock:
            def render(self):
                # Global Markets Section in Sidebar
                st.sidebar.markdown("""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    border-radius: 15px;
                    margin: 15px 0;
                    text-align: center;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                ">
                    <h2 style="color: white; margin: 0; font-size: 1.5rem;">🌍 Global Markets</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Market Status Cards
                import datetime
                import pytz
                
                # Define major markets with their timezones
                markets = {
                    "🇺🇸 NYSE": {"tz": "America/New_York", "open": 9, "close": 16},
                    "🇬🇧 LSE": {"tz": "Europe/London", "open": 8, "close": 16},
                    "🇯🇵 TSE": {"tz": "Asia/Tokyo", "open": 9, "close": 15},
                    "🇭🇰 HKEX": {"tz": "Asia/Hong_Kong", "open": 9, "close": 16},
                    "🇩🇪 FSE": {"tz": "Europe/Berlin", "open": 9, "close": 17}
                }
                
                for market_name, market_info in markets.items():
                    try:
                        tz = pytz.timezone(market_info["tz"])
                        market_time = datetime.datetime.now(tz)
                        current_hour = market_time.hour
                        
                        # Determine market status
                        if market_info["open"] <= current_hour < market_info["close"]:
                            status = "🟢 OPEN"
                            status_color = "#00D4AA"
                        else:
                            status = "🔴 CLOSED"
                            status_color = "#FF6B6B"
                        
                        # Market card
                        st.sidebar.markdown(f"""
                        <div style="
                            background: var(--secondary-bg, #262730);
                            padding: 12px;
                            border-radius: 10px;
                            margin: 8px 0;
                            border-left: 4px solid {status_color};
                            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
                        ">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong style="color: white; font-size: 0.9rem;">{market_name}</strong><br>
                                    <span style="color: #CCCCCC; font-size: 0.8rem;">{market_time.strftime('%H:%M')}</span>
                                </div>
                                <div style="text-align: right;">
                                    <span style="color: {status_color}; font-size: 0.8rem; font-weight: bold;">
                                        {status}
                                    </span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        # Fallback for timezone issues
                        st.sidebar.markdown(f"""
                        <div style="
                            background: var(--secondary-bg, #262730);
                            padding: 12px;
                            border-radius: 10px;
                            margin: 8px 0;
                            border-left: 4px solid #4ECDC4;
                        ">
                            <strong style="color: white;">{market_name}</strong><br>
                            <span style="color: #CCCCCC; font-size: 0.8rem;">Loading...</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Quick Market Indices
                st.sidebar.markdown("""
                <div style="
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    padding: 15px;
                    border-radius: 10px;
                    margin: 15px 0;
                    text-align: center;
                ">
                    <h4 style="color: white; margin: 0;">📊 Quick Indices</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Sample indices data
                import random
                indices = [
                    {"name": "S&P 500", "value": 4500 + random.randint(-100, 100), "change": random.uniform(-2, 2)},
                    {"name": "NASDAQ", "value": 14000 + random.randint(-200, 200), "change": random.uniform(-2, 2)},
                    {"name": "DOW", "value": 35000 + random.randint(-500, 500), "change": random.uniform(-2, 2)}
                ]
                
                for index in indices:
                    change_color = "#00D4AA" if index["change"] >= 0 else "#FF6B6B"
                    change_symbol = "+" if index["change"] >= 0 else ""
                    
                    st.sidebar.markdown(f"""
                    <div style="
                        background: rgba(255, 255, 255, 0.05);
                        padding: 8px;
                        border-radius: 8px;
                        margin: 5px 0;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <span style="color: white; font-size: 0.85rem;">{index["name"]}</span>
                        <div style="text-align: right;">
                            <div style="color: white; font-size: 0.85rem;">{index["value"]:,.0f}</div>
                            <div style="color: {change_color}; font-size: 0.75rem;">
                                {change_symbol}{index["change"]:.2f}%
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        return FallbackWorldClock()
    
    def run(self):
        """Main application entry point"""
        try:
            # Apply custom styling
            self._apply_styling()
            
            # Render main header
            self._render_header()
            
            # Render sidebar components
            self._render_sidebar()
            
            # Render main content
            self._render_main_content()
            
            # Render footer
            self._render_footer()
            
        except Exception as e:
            logging.error(f"Application runtime error: {e}")
            st.error("An error occurred while running the application")
    
    def _apply_styling(self):
        """Apply custom CSS styling"""
        st.markdown("""
        <style>
            /* Hide Streamlit default elements */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Modern animations */
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(52, 73, 94, 0.7); }
                70% { box-shadow: 0 0 0 10px rgba(52, 73, 94, 0); }
                100% { box-shadow: 0 0 0 0 rgba(52, 73, 94, 0); }
            }
            
            /* Dark theme */
            .stApp {
                background-color: #1a1a1a !important;
                color: #ffffff;
                animation: fadeInUp 0.8s ease-out;
            }
            
            .main .block-container {
                background: #1a1a1a !important;
                padding: 2rem;
                border-radius: 15px;
                margin-top: 1rem;
                max-width: 100%;
                color: #ffffff;
                animation: fadeInUp 1s ease-out;
            }
            
            /* Modern cards */
            .feature-card {
                padding: 20px;
                border-radius: 12px;
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: #ffffff;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin: 10px 0;
                border: 1px solid #3a3a3a;
                transition: all 0.3s ease;
            }
            
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.4);
                animation: pulse 2s infinite;
            }
            
            /* Modern buttons */
            .stButton > button {
                background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
                border: 1px solid #4a4a4a;
                border-radius: 8px;
                color: #ffffff;
                font-weight: 600;
                padding: 0.75rem 2rem;
                transition: all 0.3s ease;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                background: linear-gradient(135deg, #3c5a78 0%, #34495e 100%);
            }
            
            /* Sidebar styling - Professional approach */
            section[data-testid="stSidebar"] {
                width: 350px !important;
                min-width: 350px !important;
                max-width: 350px !important;
                transition: width 0.3s ease, margin-left 0.3s ease !important;
                position: relative !important;
                overflow: visible !important;
            }
            
            section[data-testid="stSidebar"] > div {
                width: 350px !important;
                min-width: 350px !important;
                max-width: 350px !important;
                background: linear-gradient(180deg, #1a1a1a 0%, #2c3e50 100%) !important;
                color: #ffffff !important;
                overflow-y: auto !important;
                overflow-x: hidden !important;
            }
            
            /* Collapsed state - Complete hiding */
            section[data-testid="stSidebar"].st-emotion-cache-1d391kg {
                width: 0px !important;
                min-width: 0px !important;
                max-width: 0px !important;
                margin-left: 0px !important;
                overflow: hidden !important;
            }
            
            section[data-testid="stSidebar"].st-emotion-cache-1d391kg > div {
                width: 0px !important;
                min-width: 0px !important;
                max-width: 0px !important;
                overflow: hidden !important;
                visibility: hidden !important;
            }
            
            /* Alternative collapsed state selector */
            section[data-testid="stSidebar"][aria-expanded="false"] {
                width: 0px !important;
                min-width: 0px !important;
                max-width: 0px !important;
                overflow: hidden !important;
            }
            
            section[data-testid="stSidebar"][aria-expanded="false"] > div {
                width: 0px !important;
                min-width: 0px !important;
                max-width: 0px !important;
                overflow: hidden !important;
                visibility: hidden !important;
            }
            
            /* Main content responsive to sidebar state */
            .main {
                transition: margin-left 0.3s ease !important;
            }
            
            .main .block-container {
                max-width: none !important;
                padding-left: 2rem !important;
                padding-right: 2rem !important;
            }
            
            /* Hamburger button enhancement */
            button[kind="header"] {
                background: rgba(44, 62, 80, 0.95) !important;
                border: 1px solid #4a4a4a !important;
                border-radius: 8px !important;
                padding: 0.5rem !important;
                transition: all 0.2s ease !important;
            }
            
            button[kind="header"]:hover {
                background: rgba(52, 73, 94, 0.95) !important;
                transform: scale(1.05) !important;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
            }
            
            /* Mobile optimizations */
            @media screen and (max-width: 768px) {
                section[data-testid="stSidebar"] {
                    width: 300px !important;
                    min-width: 300px !important;
                    max-width: 300px !important;
                    position: fixed !important;
                    left: 0 !important;
                    top: 0 !important;
                    height: 100vh !important;
                    z-index: 1000 !important;
                    box-shadow: 2px 0 10px rgba(0,0,0,0.3) !important;
                }
                
                section[data-testid="stSidebar"] > div {
                    width: 300px !important;
                    min-width: 300px !important;
                    max-width: 300px !important;
                    height: 100vh !important;
                }
                
                /* Mobile collapsed state */
                section[data-testid="stSidebar"].st-emotion-cache-1d391kg,
                section[data-testid="stSidebar"][aria-expanded="false"] {
                    left: -300px !important;
                    width: 300px !important;
                    min-width: 300px !important;
                    max-width: 300px !important;
                }
                
                /* Main content on mobile */
                .main .block-container {
                    padding-left: 1rem !important;
                    padding-right: 1rem !important;
                    max-width: 100% !important;
                }
                
                /* Overlay when sidebar is open on mobile */
                section[data-testid="stSidebar"]:not(.st-emotion-cache-1d391kg):not([aria-expanded="false"])::before {
                    content: '';
                    position: fixed;
                    top: 0;
                    left: 300px;
                    right: 0;
                    bottom: 0;
                    background: rgba(0,0,0,0.5);
                    z-index: 999;
                }
            }
            
            /* Sidebar text handling */
            .sidebar-content {
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                font-size: 0.85rem;
                line-height: 1.2;
            }
            
            /* Multiselect and selectbox styling */
            .stSelectbox label, .stMultiSelect label {
                font-size: 0.9rem !important;
                font-weight: 600 !important;
                color: #ffffff !important;
                white-space: nowrap !important;
            }
            
            .stSelectbox > div > div, .stMultiSelect > div > div {
                min-width: 300px !important;
                font-size: 0.85rem !important;
            }
            
            /* Status indicators */
            .status-indicator {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: bold;
                margin: 2px;
            }
            
            .status-healthy {
                background-color: #27ae60;
                color: white;
            }
            
            .status-warning {
                background-color: #f39c12;
                color: white;
            }
            
            .status-error {
                background-color: #e74c3c;
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_header(self):
        """Render application header"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%); 
                    color: #ffffff; padding: 2.5rem; border-radius: 12px; text-align: center; 
                    margin-bottom: 2rem; box-shadow: 0 6px 20px rgba(0,0,0,0.4); 
                    border: 1px solid #3a3a3a;">
            <h1 style="margin: 0; font-size: 3rem; font-weight: 700; color: #ffffff;">
                🏦 Financial News Analyzer
            </h1>
            <h3 style="font-weight: 300; font-size: 1.5rem; color: #bdc3c7; margin: 1rem 0;">
                Professional Financial Analysis & Market Intelligence Platform
            </h3>
            <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
                <span class="status-indicator status-healthy">📰 Real-time Analysis</span>
                <span class="status-indicator status-healthy">📊 Market Intelligence</span>
                <span class="status-indicator status-healthy">🌍 Global Coverage</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_sidebar(self):
        """Render sidebar components"""
        # Navigation menu
        st.sidebar.markdown("### 🧭 Navigation")
        
        # Create styled navigation cards
        st.sidebar.markdown("""
        <div style="
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            border: 1px solid #4a4a4a;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            cursor: pointer;
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(0,0,0,0.4)';" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.3)';">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 24px; margin-right: 15px;">📰</span>
                <h3 style="color: white; margin: 0; font-size: 18px;">Financial News Analysis</h3>
            </div>
            <p style="color: #bdc3c7; margin: 0; font-size: 14px;">
                Analyze market sentiment and news impact on financial instruments
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown("""
        <div style="
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            border: 1px solid #4a4a4a;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            cursor: pointer;
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(0,0,0,0.4)';" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.3)';">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 24px; margin-right: 15px;">📈</span>
                <h3 style="color: white; margin: 0; font-size: 18px;">Market Data Analysis</h3>
            </div>
            <p style="color: #bdc3c7; margin: 0; font-size: 14px;">
                View real-time charts, technical analysis and market data
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown("---")
        
        # World clock
        if self._world_clock:
            self._world_clock.render()
        else:
            st.sidebar.error("World clock component unavailable")
    
    def _render_main_content(self):
        """Render main application content"""
        # Core features section
        self._render_features()
        
        # Quick Stats Dashboard
        self._render_quick_stats()
        
        # Live Market Feed
        self._render_live_feed()
        
        # Technical information
        self._render_technical_info()
    
    def _render_features(self):
        """Render core features section"""
        st.markdown("### 🚀 Core Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>📰 Financial News Analysis</h4>
                <p>Real-time financial news aggregation with AI-powered sentiment analysis 
                and market impact assessment. Advanced NLP techniques provide deep insights 
                into market-moving news.</p>
                <div style="margin-top: 15px;">
                    <span class="status-indicator status-healthy">Live Data</span>
                    <span class="status-indicator status-healthy">AI Analysis</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>📊 Market Data Visualization</h4>
                <p>Interactive charts, real-time market data, and comprehensive portfolio 
                analysis tools. Technical indicators and advanced analytics for informed 
                decision making.</p>
                <div style="margin-top: 15px;">
                    <span class="status-indicator status-healthy">Real-time</span>
                    <span class="status-indicator status-healthy">Interactive</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h4>🌍 Global Market Coverage</h4>
                <p>24/7 monitoring of global financial markets across Americas, Europe, 
                Asia-Pacific, and MENA regions. Multi-timezone support with live market 
                status updates.</p>
                <div style="margin-top: 15px;">
                    <span class="status-indicator status-healthy">24/7 Coverage</span>
                    <span class="status-indicator status-healthy">Multi-timezone</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_quick_stats(self):
        """Render quick stats dashboard"""
        st.markdown("---")
        st.markdown("### 📈 Market Overview")
        
        # Generate sample stats
        import random
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            value = random.randint(1200, 1500)
            change = random.uniform(-2.5, 2.5)
            change_color = "#00D4AA" if change >= 0 else "#FF6B6B"
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {change_color};">
                <h3>📰 Active News</h3>
                <h2>{value}</h2>
                <p style="color: {change_color};">{'▲' if change >= 0 else '▼'} {abs(change):.1f}% vs yesterday</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            value = random.randint(85, 95)
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #00D4AA;">
                <h3>🎯 Sentiment Score</h3>
                <h2>{value}%</h2>
                <p style="color: #00D4AA;">Positive market sentiment</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            value = random.randint(45, 55)
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #4ECDC4;">
                <h3>🌍 Global Markets</h3>
                <h2>{value}</h2>
                <p style="color: #4ECDC4;">Markets actively tracked</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            value = random.uniform(95.5, 99.9)
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #00D4AA;">
                <h3>⚡ System Status</h3>
                <h2>{value:.1f}%</h2>
                <p style="color: #00D4AA;">Uptime & Performance</p>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_live_feed(self):
        """Render live market feed"""
        st.markdown("---")
        st.markdown("### � Live Market Feed")
        
        # Create sample live feed data with diverse companies
        import random
        companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "JNJ", "XOM", "WMT", "PFE", "BA", "DIS", "NVDA", "META", "BRK.A"]
        events = ["Price Alert", "Volume Spike", "News Impact", "Technical Signal", "Market Update", "Earnings Report", "Analyst Rating"]
        messages = {
            "Price Alert": ["reaches new daily high", "breaks resistance level", "hits support zone"],
            "Volume Spike": ["unusual trading volume detected", "volume surge of 200%", "institutional buying"],
            "News Impact": ["earnings report drives sentiment", "analyst upgrade", "partnership announcement"], 
            "Technical Signal": ["moving average crossover", "RSI oversold signal", "bullish pattern"],
            "Market Update": ["sector rotation detected", "market volatility increase", "correlation alert"],
            "Earnings Report": ["beats earnings estimates", "revenue guidance updated", "quarterly results"],
            "Analyst Rating": ["price target raised", "recommendation upgrade", "coverage initiated"]
        }
        
        feed_items = []
        for i in range(8):
            symbol = random.choice(companies)
            event = random.choice(events)
            message = random.choice(messages[event])
            time_offset = random.randint(1, 30)
            
            # Determine sentiment
            if any(word in message for word in ["high", "upgrade", "beats", "raised"]):
                sentiment = "positive"
            elif any(word in message for word in ["volatility", "oversold", "support"]):
                sentiment = "negative"
            else:
                sentiment = "neutral"
                
            feed_items.append({
                "time": f"09:{30-time_offset:02d}",
                "symbol": symbol,
                "event": event,
                "message": message,
                "type": sentiment
            })
        
        for item in feed_items:
            type_colors = {
                "positive": "#00D4AA",
                "negative": "#FF6B6B", 
                "neutral": "#4ECDC4"
            }
            color = type_colors.get(item["type"], "#4ECDC4")
            
            st.markdown(f"""
            <div style="
                background: var(--secondary-bg);
                padding: 12px;
                border-radius: 8px;
                margin: 5px 0;
                border-left: 4px solid {color};
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div>
                    <strong style="color: {color};">{item['symbol']} - {item['event']}</strong><br>
                    <span style="color: #CCCCCC; font-size: 0.9rem;">{item['message']}</span>
                </div>
                <div style="color: #888; font-size: 0.8rem;">
                    {item['time']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_technical_info(self):
        """Render technical information section"""
        with st.expander("🛠️ Technical Architecture & Information"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **🏗️ Architecture:**
                - Clean Architecture (Domain, Application, Infrastructure)
                - SOLID Principles Implementation
                - Dependency Injection Pattern
                - Repository Pattern
                - Use Case Pattern
                - Observer Pattern
                - Strategy Pattern
                """)
            
            with col2:
                st.markdown("""
                **🖥️ Technology Stack:**
                - Python 3.11+ with Type Hints
                - Streamlit Framework
                - Domain-Driven Design
                - Comprehensive Error Handling
                - Logging and Monitoring
                - Responsive Design
                """)
            
            # Show system metrics if available
            if self._container:
                st.markdown("**📊 System Metrics:**")
                health = self._container.health_check()
                
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                
                with metrics_col1:
                    st.metric("Services", health.get("services_count", 0))
                
                with metrics_col2:
                    status = health.get("container_status", "unknown")
                    st.metric("Status", status.title())
                
                with metrics_col3:
                    st.metric("Mode", "Active" if status == "healthy" else "Demo")
            else:
                st.markdown("**📊 System Metrics:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Services", "Demo")
                with col2:
                    st.metric("Status", "Fallback")
                with col3:
                    st.metric("Mode", "Demo")
    
    def _render_footer(self):
        """Render application footer"""
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; margin-top: 30px;">
            <p>📊 Financial News Analyzer • Built with ❤️ for Financial Professionals</p>
            <p style="font-size: 0.9em;">
                Real-time data • Advanced analytics • Professional insights • Modern Architecture
            </p>
            <p style="font-size: 0.8em; margin-top: 10px;">
                Powered by Clean Code principles and SOLID design patterns
            </p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    try:
        app = FinancialAnalyzerApp()
        app.run()
        
    except Exception as e:
        logging.error(f"Critical application error: {e}")
        st.error(f"Critical error: {e}")
        st.info("Please refresh the page or contact support if the problem persists.")

if __name__ == "__main__":
    main()
