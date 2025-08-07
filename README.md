# 🏦 Financial News Analyzer

<div align="center">

![Financial News Analyzer](https://img.shields.io/badge/Financial-News%20Analyzer-2c3e50?style=for-the-badge&logo=chart-line)
![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Professional Financial Analysis & Market Intelligence Platform with Google Sheets Feedback System**

🌐 **Live Demo:** [financialnewsanalyzer.streamlit.app](https://financialnewsanalyzer.streamlit.app/)

*Advanced AI-powered financial news sentiment analysis with real-time market data visualization*

[🚀 Demo](#demo) • [📖 Documentation](#documentation) • [⚡ Quick Start](#quick-start) • [🔧 Features](#features)

</div>

---

## 🌟 Overview

Financial News Analyzer is a cutting-edge financial intelligence platform that combines **AI-powered sentiment analysis**, **real-time market data**, and **interactive visualizations** to provide comprehensive market insights. Built with modern architecture principles and designed for financial professionals, traders, and analysts.

### 🎯 Key Highlights

- **🤖 AI-Powered Analysis**: Advanced NLP algorithms for news sentiment analysis
- **📊 Real-time Data**: Live market data with interactive charts and technical indicators
- **🌍 Global Coverage**: 24/7 monitoring across Americas, Europe, Asia-Pacific, and MENA
- **📱 Responsive Design**: Modern UI with professional animations and dark theme
- **🏗️ Clean Architecture**: SOLID principles with layered design pattern
- **⚡ High Performance**: Optimized data processing and caching mechanisms

## 🔧 Features

### 📰 Financial News Analysis
- **Sentiment Analysis**: AI-powered sentiment scoring for market-moving news
- **Company-specific Insights**: Targeted analysis for individual stocks and companies
- **News Aggregation**: Real-time news feed from multiple financial sources
- **Impact Assessment**: Market impact prediction based on news sentiment
- **Historical Trends**: Sentiment timeline analysis and pattern recognition

### 📈 Market Data Visualization
- **Interactive Charts**: Candlestick, line, and area charts with zoom functionality
- **Technical Indicators**: Moving averages, RSI, MACD, and custom indicators
- **Portfolio Analysis**: Comprehensive portfolio performance tracking
- **Market Overview**: Real-time market status across global exchanges
- **Correlation Analysis**: Inter-market and cross-asset correlation matrices

### 🌍 Global Market Coverage
- **Multi-timezone Support**: Live market status across different time zones
- **Regional Analysis**: Dedicated coverage for major financial regions
- **Currency Tracking**: Real-time forex rates and currency analysis
- **Commodity Data**: Oil, gold, and other commodity price tracking
- **Economic Indicators**: Key economic metrics and calendar events

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended)
- Google Cloud Service Account (for feedback system)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/enecpp/FINANCIALNEWSANALYZER.git
   cd FINANCIALNEWSANALYZER/financial_news_analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Streamlit Secrets (for feedback system)**
   - Copy `.streamlit/secrets.toml.template` to `.streamlit/secrets.toml`
   - Follow the setup guide in `STREAMLIT_CLOUD_SECRETS.md`
   - Or see `FEEDBACK_SETUP.md` for detailed Google Sheets integration

5. **Launch the application**
   ```bash
   streamlit run Start.py
   ```

6. **Access the platform**
   - Open your browser and navigate to `http://localhost:8501`
   - Enjoy the comprehensive financial analysis experience!

## 📋 Requirements

```
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
numpy>=1.24.0
pytz>=2023.3
python-dateutil>=2.8.2
gspread>=5.12.0
google-auth>=2.22.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
```

## 🔐 Security & Configuration

**Important:** This project uses Google Sheets for feedback storage. For security:

- 📋 **Setup Guide**: See `FEEDBACK_SETUP.md` for detailed configuration
- 🚀 **Streamlit Cloud**: See `STREAMLIT_CLOUD_SECRETS.md` for cloud deployment
- 🛡️ **Security**: Never commit API keys to Git (already configured in `.gitignore`)
- 📝 **Template**: Use `.streamlit/secrets.toml.template` as reference

The feedback system safely stores user messages in Google Sheets with CSV fallback.

## 🏗️ Architecture

The Financial News Analyzer follows **Clean Architecture** principles with a well-organized structure:

```
financial_news_analyzer/
├── 📁 src/
│   ├── 📁 application/          # Application business logic
│   ├── 📁 domain/               # Core domain entities
│   ├── 📁 infrastructure/       # External integrations
│   └── 📁 presentation/         # UI components
├── 📁 pages/                    # Streamlit pages
│   ├── 1_Financial_Analysis.py  # News sentiment analysis
│   └── 2_Market_Data.py         # Market data visualization
├── 📁 config/                   # Configuration files
├── 📁 tests/                    # Unit and integration tests
├── Start.py                     # Main application entry point
└── requirements.txt             # Python dependencies
```

### 🎨 Design Principles

- **SOLID Principles**: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Clean Architecture**: Domain-driven design with clear separation of concerns
- **Dependency Injection**: Loose coupling through dependency injection container
- **Use Case Pattern**: Business logic encapsulated in specific use cases
- **Repository Pattern**: Data access abstraction for external services

## 🎮 Usage Examples

### 📊 Analyzing Company Sentiment

```python
# Select a company from the extensive database
selected_company = "Apple Inc. (AAPL)"

# View real-time sentiment analysis
sentiment_score = analyzer.get_sentiment(selected_company)
market_impact = analyzer.assess_impact(sentiment_score)

# Generate insights and recommendations
insights = analyzer.generate_insights(selected_company)
```

### 📈 Market Data Analysis

```python
# Track market performance
market_data = analyzer.get_market_overview()
technical_indicators = analyzer.calculate_indicators(symbol="AAPL")

# Generate interactive visualizations
chart = analyzer.create_interactive_chart(
    symbol="AAPL",
    indicators=["SMA", "EMA", "RSI"],
    timeframe="1M"
)
```

## 🌟 Screenshots

### Main Dashboard
![Main Dashboard](https://via.placeholder.com/800x400/2c3e50/ffffff?text=Financial+News+Analyzer+Dashboard)

### Financial Analysis Page
![Financial Analysis](https://via.placeholder.com/800x400/34495e/ffffff?text=AI-Powered+Sentiment+Analysis)

### Market Data Visualization
![Market Data](https://via.placeholder.com/800x400/1a1a1a/ffffff?text=Real-time+Market+Data)

## 🔮 Roadmap

### 🎯 Upcoming Features

- [ ] **Machine Learning Models**: Advanced predictive models for price forecasting
- [ ] **API Integration**: Real-time data feeds from Bloomberg, Reuters, Alpha Vantage
- [ ] **Mobile App**: React Native mobile application
- [ ] **Alerts System**: Email and SMS notifications for market events
- [ ] **Portfolio Management**: Advanced portfolio tracking and optimization
- [ ] **Social Sentiment**: Twitter and Reddit sentiment integration
- [ ] **Backtesting Engine**: Strategy backtesting with historical data
- [ ] **Multi-language Support**: International language support

### 🚀 Performance Enhancements

- [ ] **Redis Caching**: Advanced caching for improved performance
- [ ] **Database Integration**: PostgreSQL for data persistence
- [ ] **Microservices**: Dockerized microservices architecture
- [ ] **Load Balancing**: Horizontal scaling capabilities

## 🤝 Contributing

We welcome contributions from the financial technology community! Here's how you can contribute:

### 🛠️ Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests for new functionality**
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### 📝 Contribution Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for any API changes
- Ensure all tests pass before submitting
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

<div align="center">

**Built with ❤️ by Financial Technology Enthusiasts**

[![GitHub](https://img.shields.io/badge/GitHub-enecpp-181717?style=flat-square&logo=github)](https://github.com/enecpp)

</div>

## 🙏 Acknowledgments

- **Streamlit Team** for the amazing web app framework
- **Plotly Team** for powerful visualization capabilities
- **Financial Data Providers** for market data access
- **Open Source Community** for continuous inspiration

## 📞 Support

Need help? We're here for you!

- 📧 **Email**: enesor8@gmail.com
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/enecpp/FINANCIALNEWSANALYZER/issues)
- 📋 **Setup Help**: Check `FEEDBACK_SETUP.md` and `STREAMLIT_CLOUD_SECRETS.md`
- 🔐 **Security**: All sensitive data is properly secured and not exposed in repository

---

<div align="center">

**⭐ If you find this project helpful, please give it a star! ⭐**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=enecpp.mleng-financial_news_analyzer)

</div>
