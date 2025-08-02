"""
Financial News Entity
Represents a financial news article with analysis capabilities
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

class NewsCategory(Enum):
    """Categories for financial news"""
    MARKET_ANALYSIS = "market_analysis"
    EARNINGS = "earnings"
    ECONOMIC_INDICATORS = "economic_indicators"
    CORPORATE_NEWS = "corporate_news"
    GLOBAL_MARKETS = "global_markets"
    CRYPTOCURRENCY = "cryptocurrency"
    COMMODITIES = "commodities"
    REGULATORY = "regulatory"

class NewsSource(Enum):
    """News source types"""
    REUTERS = "reuters"
    BLOOMBERG = "bloomberg"
    FINANCIAL_TIMES = "financial_times"
    WALL_STREET_JOURNAL = "wall_street_journal"
    YAHOO_FINANCE = "yahoo_finance"
    MARKETWATCH = "marketwatch"
    CNBC = "cnbc"
    OTHER = "other"

@dataclass
class FinancialNews:
    """
    Core entity representing a financial news article
    
    Follows SOLID principles:
    - Single Responsibility: Represents news data only
    - Open/Closed: Extensible via inheritance
    - Liskov Substitution: Can be substituted by subclasses
    - Interface Segregation: Clean, focused interface
    - Dependency Inversion: Depends on abstractions (enums)
    """
    
    # Core identifiers
    id: str
    title: str
    content: str
    
    # Metadata
    source: NewsSource
    category: NewsCategory
    published_at: datetime
    created_at: Optional[datetime] = None
    
    # Content analysis
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    mentioned_symbols: Optional[List[str]] = None
    
    # Metrics
    sentiment_score: Optional[float] = None  # -1.0 to 1.0
    confidence_score: Optional[float] = None  # 0.0 to 1.0
    impact_score: Optional[float] = None  # 0.0 to 1.0
    
    # Additional data
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize computed fields"""
        if self.created_at is None:
            self.created_at = datetime.now()
        
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def is_positive_sentiment(self) -> bool:
        """Check if news has positive sentiment"""
        return self.sentiment_score is not None and self.sentiment_score > 0.1
    
    @property
    def is_negative_sentiment(self) -> bool:
        """Check if news has negative sentiment"""
        return self.sentiment_score is not None and self.sentiment_score < -0.1
    
    @property
    def is_neutral_sentiment(self) -> bool:
        """Check if news has neutral sentiment"""
        return self.sentiment_score is not None and -0.1 <= self.sentiment_score <= 0.1
    
    @property
    def is_high_impact(self) -> bool:
        """Check if news has high market impact"""
        return self.impact_score is not None and self.impact_score > 0.7
    
    @property
    def is_reliable(self) -> bool:
        """Check if analysis is reliable based on confidence"""
        return self.confidence_score is not None and self.confidence_score > 0.6
    
    def get_sentiment_label(self) -> str:
        """Get human-readable sentiment label"""
        if self.sentiment_score is None:
            return "Unknown"
        
        if self.is_positive_sentiment:
            return "Positive"
        elif self.is_negative_sentiment:
            return "Negative"
        else:
            return "Neutral"
    
    def get_impact_label(self) -> str:
        """Get human-readable impact label"""
        if self.impact_score is None:
            return "Unknown"
        
        if self.impact_score > 0.7:
            return "High"
        elif self.impact_score > 0.4:
            return "Medium"
        else:
            return "Low"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'source': self.source.value,
            'category': self.category.value,
            'published_at': self.published_at.isoformat(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'summary': self.summary,
            'keywords': self.keywords,
            'mentioned_symbols': self.mentioned_symbols,
            'sentiment_score': self.sentiment_score,
            'confidence_score': self.confidence_score,
            'impact_score': self.impact_score,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FinancialNews':
        """Create instance from dictionary"""
        return cls(
            id=data['id'],
            title=data['title'],
            content=data['content'],
            source=NewsSource(data['source']),
            category=NewsCategory(data['category']),
            published_at=datetime.fromisoformat(data['published_at']),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            summary=data.get('summary'),
            keywords=data.get('keywords'),
            mentioned_symbols=data.get('mentioned_symbols'),
            sentiment_score=data.get('sentiment_score'),
            confidence_score=data.get('confidence_score'),
            impact_score=data.get('impact_score'),
            metadata=data.get('metadata', {})
        )
    
    def __str__(self) -> str:
        """String representation"""
        return f"FinancialNews(id={self.id}, title='{self.title[:50]}...', source={self.source.value})"
    
    def __repr__(self) -> str:
        """Developer representation"""
        return self.__str__()
