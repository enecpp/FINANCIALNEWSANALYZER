"""
Mock News Service
Provides sample news data for development and testing
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import random

class MockNewsService:
    """Mock service for financial news data"""
    
    def __init__(self):
        self.companies = [
            'Apple Inc.', 'Microsoft Corp.', 'Amazon.com Inc.', 'Alphabet Inc.',
            'Tesla Inc.', 'Meta Platforms Inc.', 'Netflix Inc.', 'NVIDIA Corp.'
        ]
        self.news_sources = [
            'Reuters', 'Bloomberg', 'Financial Times', 'Wall Street Journal',
            'CNBC', 'MarketWatch', 'Yahoo Finance', 'Seeking Alpha'
        ]
        self.news_categories = [
            'Earnings', 'Product Launch', 'Merger & Acquisition', 'Partnership',
            'Regulation', 'Market Analysis', 'Leadership Change', 'Innovation'
        ]
    
    def get_latest_news(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get latest financial news"""
        news_items = []
        
        for i in range(limit):
            company = random.choice(self.companies)
            source = random.choice(self.news_sources)
            category = random.choice(self.news_categories)
            
            # Generate realistic sentiment
            sentiment_score = random.uniform(-1.0, 1.0)
            if sentiment_score > 0.2:
                sentiment = 'Positive'
            elif sentiment_score < -0.2:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
            
            # Generate sample headline
            headlines = {
                'Earnings': f"{company} Reports {random.choice(['Strong', 'Weak', 'Mixed'])} Q{random.randint(1,4)} Earnings",
                'Product Launch': f"{company} Unveils {random.choice(['Revolutionary', 'New', 'Updated'])} Product Line",
                'Merger & Acquisition': f"{company} {random.choice(['Acquires', 'Merges with', 'Partners with'])} Tech Startup",
                'Partnership': f"{company} Forms Strategic Partnership with Industry Leader",
                'Regulation': f"New Regulations Impact {company}'s Operations",
                'Market Analysis': f"Analysts {random.choice(['Upgrade', 'Downgrade', 'Maintain'])} {company} Rating",
                'Leadership Change': f"{company} Announces {random.choice(['CEO', 'CFO', 'CTO'])} Transition",
                'Innovation': f"{company} Breakthrough in {random.choice(['AI', 'Cloud', 'Hardware'])} Technology"
            }
            
            news_item = {
                'id': f"news_{i+1}",
                'headline': headlines.get(category, f"{company} News Update"),
                'company': company,
                'source': source,
                'category': category,
                'sentiment': sentiment,
                'sentiment_score': round(sentiment_score, 3),
                'impact_score': round(random.uniform(0.1, 1.0), 3),
                'published_at': (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
                'url': f"https://example.com/news/{i+1}",
                'summary': f"Latest developments from {company} regarding {category.lower()}..."
            }
            
            news_items.append(news_item)
        
        return sorted(news_items, key=lambda x: x['published_at'], reverse=True)
    
    def get_company_news(self, company: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get news for a specific company"""
        all_news = self.get_latest_news(50)
        company_news = [news for news in all_news if company.lower() in news['company'].lower()]
        return company_news[:limit]
    
    def get_sentiment_analysis(self, period_days: int = 30) -> Dict[str, Any]:
        """Get sentiment analysis for the specified period"""
        news_items = self.get_latest_news(100)
        
        # Filter by date range
        cutoff_date = datetime.now() - timedelta(days=period_days)
        recent_news = [
            news for news in news_items 
            if datetime.fromisoformat(news['published_at']) > cutoff_date
        ]
        
        if not recent_news:
            return {'error': 'No news found for the specified period'}
        
        # Calculate sentiment statistics
        sentiments = [news['sentiment_score'] for news in recent_news]
        sentiment_counts = {}
        for news in recent_news:
            sentiment = news['sentiment']
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        return {
            'total_articles': len(recent_news),
            'average_sentiment': round(sum(sentiments) / len(sentiments), 3),
            'sentiment_distribution': sentiment_counts,
            'period_days': period_days,
            'most_active_source': max(set([news['source'] for news in recent_news]), 
                                    key=[news['source'] for news in recent_news].count),
            'dominant_category': max(set([news['category'] for news in recent_news]), 
                                   key=[news['category'] for news in recent_news].count)
        }

# Create instance for export
mock_news_service = MockNewsService()
