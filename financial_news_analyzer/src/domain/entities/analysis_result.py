"""
Analysis Result Entities
Represents the results of financial analysis operations
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from enum import Enum

class SentimentType(Enum):
    """Types of sentiment analysis"""
    VERY_NEGATIVE = "very_negative"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    VERY_POSITIVE = "very_positive"

class AnalysisType(Enum):
    """Types of analysis performed"""
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    TECHNICAL_ANALYSIS = "technical_analysis"
    FUNDAMENTAL_ANALYSIS = "fundamental_analysis"
    NEWS_IMPACT_ANALYSIS = "news_impact_analysis"
    MARKET_CORRELATION = "market_correlation"

@dataclass
class SentimentScore:
    """
    Detailed sentiment scoring with confidence metrics
    
    Clean Code Principles:
    - Descriptive naming for clarity
    - Immutable data structure
    - Clear validation rules
    """
    
    # Core sentiment data
    score: float  # -1.0 (very negative) to 1.0 (very positive)
    confidence: float  # 0.0 to 1.0
    sentiment_type: SentimentType
    
    # Detailed breakdown
    positive_probability: Optional[float] = None
    negative_probability: Optional[float] = None
    neutral_probability: Optional[float] = None
    
    # Analysis metadata
    analyzed_text_length: Optional[int] = None
    key_phrases: Optional[List[str]] = None
    
    def __post_init__(self):
        """Validate sentiment score bounds"""
        if not -1.0 <= self.score <= 1.0:
            raise ValueError("Sentiment score must be between -1.0 and 1.0")
        
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        
        # Auto-determine sentiment type if not provided
        if self.sentiment_type is None:
            self.sentiment_type = self._determine_sentiment_type()
    
    def _determine_sentiment_type(self) -> SentimentType:
        """Determine sentiment type based on score"""
        if self.score <= -0.6:
            return SentimentType.VERY_NEGATIVE
        elif self.score <= -0.2:
            return SentimentType.NEGATIVE
        elif self.score <= 0.2:
            return SentimentType.NEUTRAL
        elif self.score <= 0.6:
            return SentimentType.POSITIVE
        else:
            return SentimentType.VERY_POSITIVE
    
    @property
    def is_reliable(self) -> bool:
        """Check if sentiment analysis is reliable"""
        return self.confidence >= 0.7
    
    @property
    def sentiment_emoji(self) -> str:
        """Get emoji representation of sentiment"""
        emoji_map = {
            SentimentType.VERY_NEGATIVE: "😢",
            SentimentType.NEGATIVE: "😟",
            SentimentType.NEUTRAL: "😐",
            SentimentType.POSITIVE: "😊",
            SentimentType.VERY_POSITIVE: "😄"
        }
        return emoji_map.get(self.sentiment_type, "❓")
    
    @property
    def color_code(self) -> str:
        """Get color code for visualization"""
        color_map = {
            SentimentType.VERY_NEGATIVE: "#FF4444",
            SentimentType.NEGATIVE: "#FF8888",
            SentimentType.NEUTRAL: "#FFAA00",
            SentimentType.POSITIVE: "#88FF88",
            SentimentType.VERY_POSITIVE: "#44FF44"
        }
        return color_map.get(self.sentiment_type, "#CCCCCC")

@dataclass
class AnalysisResult:
    """
    Comprehensive analysis result container
    
    OOP Design Patterns:
    - Builder pattern for complex construction
    - Strategy pattern for different analysis types
    - Observer pattern for result notifications
    """
    
    # Core identification (required fields first)
    id: str
    analysis_type: AnalysisType
    subject_id: str  # ID of analyzed entity (news, stock, etc.)
    
    # Analysis results (optional fields with defaults)
    sentiment_score: Optional[SentimentScore] = None
    impact_score: Optional[float] = None  # 0.0 to 1.0
    confidence_level: Optional[float] = None  # 0.0 to 1.0
    
    # Detailed insights
    summary: Optional[str] = None
    key_insights: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    
    # Risk assessment
    risk_level: Optional[str] = None  # "low", "medium", "high"
    risk_factors: Optional[List[str]] = None
    
    # Technical details
    analysis_method: Optional[str] = None
    data_sources: Optional[List[str]] = None
    processing_time_ms: Optional[int] = None
    
    # Metadata (created_at default olarak datetime.now() kullanacak)
    created_at: datetime = None  # Will be set in __post_init__
    analyst: Optional[str] = None  # Human or AI analyst identifier
    version: str = "1.0"
    
    # Additional data
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize computed fields"""
        if self.metadata is None:
            self.metadata = {}
        
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @property
    def overall_sentiment(self) -> str:
        """Get overall sentiment description"""
        if self.sentiment_score is None:
            return "Unknown"
        return f"{self.sentiment_score.sentiment_emoji} {self.sentiment_score.sentiment_type.value.replace('_', ' ').title()}"
    
    @property
    def is_high_impact(self) -> bool:
        """Check if analysis indicates high market impact"""
        return self.impact_score is not None and self.impact_score > 0.7
    
    @property
    def is_reliable_analysis(self) -> bool:
        """Check if analysis results are reliable"""
        return (
            self.confidence_level is not None and 
            self.confidence_level > 0.6 and
            (self.sentiment_score is None or self.sentiment_score.is_reliable)
        )
    
    @property
    def risk_color(self) -> str:
        """Get color code for risk level"""
        color_map = {
            "low": "#28a745",
            "medium": "#ffc107", 
            "high": "#dc3545"
        }
        return color_map.get(self.risk_level, "#6c757d")
    
    def add_insight(self, insight: str):
        """Add a key insight to the analysis"""
        if self.key_insights is None:
            self.key_insights = []
        self.key_insights.append(insight)
    
    def add_recommendation(self, recommendation: str):
        """Add a recommendation based on analysis"""
        if self.recommendations is None:
            self.recommendations = []
        self.recommendations.append(recommendation)
    
    def add_risk_factor(self, risk_factor: str):
        """Add a risk factor"""
        if self.risk_factors is None:
            self.risk_factors = []
        self.risk_factors.append(risk_factor)
    
    def set_risk_level(self, level: str):
        """Set risk level with validation"""
        valid_levels = ["low", "medium", "high"]
        if level.lower() not in valid_levels:
            raise ValueError(f"Risk level must be one of: {valid_levels}")
        self.risk_level = level.lower()
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics of the analysis"""
        return {
            "analysis_type": self.analysis_type.value,
            "overall_sentiment": self.overall_sentiment,
            "impact_score": self.impact_score,
            "confidence_level": self.confidence_level,
            "risk_level": self.risk_level,
            "insights_count": len(self.key_insights) if self.key_insights else 0,
            "recommendations_count": len(self.recommendations) if self.recommendations else 0,
            "is_reliable": self.is_reliable_analysis,
            "is_high_impact": self.is_high_impact,
            "created_at": self.created_at.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        result = {
            "id": self.id,
            "analysis_type": self.analysis_type.value,
            "subject_id": self.subject_id,
            "impact_score": self.impact_score,
            "confidence_level": self.confidence_level,
            "summary": self.summary,
            "key_insights": self.key_insights,
            "recommendations": self.recommendations,
            "risk_level": self.risk_level,
            "risk_factors": self.risk_factors,
            "analysis_method": self.analysis_method,
            "data_sources": self.data_sources,
            "processing_time_ms": self.processing_time_ms,
            "created_at": self.created_at.isoformat(),
            "analyst": self.analyst,
            "version": self.version,
            "metadata": self.metadata
        }
        
        if self.sentiment_score:
            result["sentiment_score"] = {
                "score": self.sentiment_score.score,
                "confidence": self.sentiment_score.confidence,
                "sentiment_type": self.sentiment_score.sentiment_type.value,
                "positive_probability": self.sentiment_score.positive_probability,
                "negative_probability": self.sentiment_score.negative_probability,
                "neutral_probability": self.sentiment_score.neutral_probability,
                "analyzed_text_length": self.sentiment_score.analyzed_text_length,
                "key_phrases": self.sentiment_score.key_phrases
            }
        
        return result
    
    def __str__(self) -> str:
        """String representation"""
        return f"AnalysisResult(id={self.id}, type={self.analysis_type.value}, sentiment={self.overall_sentiment})"
    
    def __repr__(self) -> str:
        """Developer representation"""
        return self.__str__()
