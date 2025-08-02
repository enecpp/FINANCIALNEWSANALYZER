"""
Sentiment Analysis Service
Advanced sentiment analysis for financial texts
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import re
from datetime import datetime

from ..entities.analysis_result import SentimentScore, SentimentType, AnalysisResult, AnalysisType
from ..entities.financial_news import FinancialNews

class ISentimentAnalyzer(ABC):
    """
    Interface for sentiment analysis implementations
    
    SOLID Principles:
    - Interface Segregation: Clean, focused interface
    - Dependency Inversion: Depend on abstraction
    """
    
    @abstractmethod
    def analyze_text(self, text: str) -> SentimentScore:
        """Analyze sentiment of given text"""
        pass
    
    @abstractmethod
    def analyze_batch(self, texts: List[str]) -> List[SentimentScore]:
        """Analyze sentiment of multiple texts"""
        pass

class FinancialSentimentAnalyzer(ISentimentAnalyzer):
    """
    Financial-specific sentiment analyzer
    
    Clean Code Principles:
    - Single Responsibility: Only handles sentiment analysis
    - DRY: Reusable analysis methods
    - Meaningful names for all methods
    """
    
    def __init__(self):
        """Initialize with financial sentiment keywords"""
        self._positive_keywords = {
            'growth', 'profit', 'gain', 'increase', 'rise', 'bull', 'bullish', 
            'positive', 'strong', 'robust', 'outperform', 'exceed', 'beat',
            'surge', 'rally', 'boom', 'upturn', 'recovery', 'expand', 'improve',
            'optimistic', 'confident', 'breakthrough', 'milestone', 'record',
            'success', 'achievement', 'upward', 'buy', 'upgrade', 'recommend'
        }
        
        self._negative_keywords = {
            'loss', 'decline', 'fall', 'drop', 'bear', 'bearish', 'negative',
            'weak', 'poor', 'underperform', 'miss', 'fail', 'crash', 'plunge',
            'collapse', 'recession', 'downturn', 'crisis', 'risk', 'concern',
            'worry', 'pessimistic', 'uncertainty', 'volatile', 'sell', 'downgrade',
            'warning', 'threat', 'challenge', 'struggle', 'bankruptcy', 'debt'
        }
        
        self._neutral_keywords = {
            'stable', 'maintain', 'hold', 'unchanged', 'steady', 'flat',
            'neutral', 'sideways', 'consolidate', 'range', 'monitor', 'watch'
        }
    
    def analyze_text(self, text: str) -> SentimentScore:
        """
        Analyze sentiment of financial text
        
        Args:
            text: Text to analyze
            
        Returns:
            SentimentScore with detailed analysis
        """
        if not text or not text.strip():
            return SentimentScore(
                score=0.0,
                confidence=0.0,
                sentiment_type=SentimentType.NEUTRAL,
                analyzed_text_length=0
            )
        
        # Clean and normalize text
        clean_text = self._preprocess_text(text)
        
        # Extract key phrases
        key_phrases = self._extract_key_phrases(clean_text)
        
        # Calculate sentiment scores
        positive_score = self._calculate_positive_score(clean_text)
        negative_score = self._calculate_negative_score(clean_text)
        neutral_score = self._calculate_neutral_score(clean_text)
        
        # Normalize scores
        total_score = positive_score + negative_score + neutral_score
        if total_score > 0:
            positive_prob = positive_score / total_score
            negative_prob = negative_score / total_score
            neutral_prob = neutral_score / total_score
        else:
            positive_prob = negative_prob = neutral_prob = 0.33
        
        # Calculate final sentiment score
        final_score = positive_prob - negative_prob
        
        # Calculate confidence based on score distribution
        confidence = self._calculate_confidence(positive_prob, negative_prob, neutral_prob)
        
        # Determine sentiment type
        sentiment_type = self._determine_sentiment_type(final_score)
        
        return SentimentScore(
            score=final_score,
            confidence=confidence,
            sentiment_type=sentiment_type,
            positive_probability=positive_prob,
            negative_probability=negative_prob,
            neutral_probability=neutral_prob,
            analyzed_text_length=len(text),
            key_phrases=key_phrases[:10]  # Top 10 key phrases
        )
    
    def analyze_batch(self, texts: List[str]) -> List[SentimentScore]:
        """Analyze sentiment of multiple texts efficiently"""
        return [self.analyze_text(text) for text in texts]
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces and basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key financial phrases from text"""
        words = text.split()
        phrases = []
        
        # Extract individual keywords
        for word in words:
            word = word.strip('.,!?')
            if (word in self._positive_keywords or 
                word in self._negative_keywords or 
                word in self._neutral_keywords):
                phrases.append(word)
        
        # Extract common financial phrases
        financial_phrases = [
            'earnings per share', 'market cap', 'revenue growth', 'profit margin',
            'cash flow', 'return on investment', 'price target', 'analyst rating',
            'market share', 'competitive advantage', 'debt to equity'
        ]
        
        for phrase in financial_phrases:
            if phrase in text:
                phrases.append(phrase)
        
        return list(set(phrases))  # Remove duplicates
    
    def _calculate_positive_score(self, text: str) -> float:
        """Calculate positive sentiment score"""
        words = text.split()
        score = 0.0
        
        for word in words:
            word = word.strip('.,!?')
            if word in self._positive_keywords:
                score += 1.0
        
        # Apply context boosters
        if 'very' in text or 'extremely' in text or 'significantly' in text:
            score *= 1.2
        
        return score
    
    def _calculate_negative_score(self, text: str) -> float:
        """Calculate negative sentiment score"""
        words = text.split()
        score = 0.0
        
        for word in words:
            word = word.strip('.,!?')
            if word in self._negative_keywords:
                score += 1.0
        
        # Apply context boosters
        if 'very' in text or 'extremely' in text or 'significantly' in text:
            score *= 1.2
        
        return score
    
    def _calculate_neutral_score(self, text: str) -> float:
        """Calculate neutral sentiment score"""
        words = text.split()
        score = 0.0
        
        for word in words:
            word = word.strip('.,!?')
            if word in self._neutral_keywords:
                score += 1.0
        
        return score
    
    def _calculate_confidence(self, pos_prob: float, neg_prob: float, neut_prob: float) -> float:
        """Calculate confidence score based on probability distribution"""
        # Higher confidence when one sentiment clearly dominates
        max_prob = max(pos_prob, neg_prob, neut_prob)
        
        # Calculate entropy (lower entropy = higher confidence)
        import math
        probs = [p for p in [pos_prob, neg_prob, neut_prob] if p > 0]
        entropy = -sum(p * math.log(p) for p in probs) if probs else 0
        max_entropy = math.log(3)  # Maximum entropy for 3 categories
        
        # Convert entropy to confidence (0 = low confidence, 1 = high confidence)
        confidence = 1 - (entropy / max_entropy) if max_entropy > 0 else 0
        
        # Boost confidence if dominant sentiment is strong
        if max_prob > 0.6:
            confidence *= 1.2
        
        return min(confidence, 1.0)
    
    def _determine_sentiment_type(self, score: float) -> SentimentType:
        """Determine sentiment type from score"""
        if score <= -0.6:
            return SentimentType.VERY_NEGATIVE
        elif score <= -0.2:
            return SentimentType.NEGATIVE
        elif score <= 0.2:
            return SentimentType.NEUTRAL
        elif score <= 0.6:
            return SentimentType.POSITIVE
        else:
            return SentimentType.VERY_POSITIVE

class SentimentAnalysisService:
    """
    Service for managing sentiment analysis operations
    
    Design Patterns:
    - Strategy Pattern: Different analyzers for different domains
    - Factory Pattern: Creates appropriate analyzer instances
    """
    
    def __init__(self, analyzer: Optional[ISentimentAnalyzer] = None):
        """Initialize service with analyzer"""
        self._analyzer = analyzer or FinancialSentimentAnalyzer()
    
    def analyze_news(self, news: FinancialNews) -> AnalysisResult:
        """
        Perform comprehensive sentiment analysis on financial news
        
        Args:
            news: Financial news article to analyze
            
        Returns:
            Complete analysis result with sentiment and insights
        """
        # Analyze title and content separately
        title_sentiment = self._analyzer.analyze_text(news.title)
        content_sentiment = self._analyzer.analyze_text(news.content)
        
        # Combine sentiments (title weighted more heavily)
        combined_score = (title_sentiment.score * 0.4) + (content_sentiment.score * 0.6)
        combined_confidence = (title_sentiment.confidence + content_sentiment.confidence) / 2
        
        # Create comprehensive sentiment score
        combined_sentiment = SentimentScore(
            score=combined_score,
            confidence=combined_confidence,
            sentiment_type=self._analyzer._determine_sentiment_type(combined_score),
            positive_probability=(title_sentiment.positive_probability + content_sentiment.positive_probability) / 2,
            negative_probability=(title_sentiment.negative_probability + content_sentiment.negative_probability) / 2,
            neutral_probability=(title_sentiment.neutral_probability + content_sentiment.neutral_probability) / 2,
            analyzed_text_length=len(news.title) + len(news.content),
            key_phrases=list(set((title_sentiment.key_phrases or []) + (content_sentiment.key_phrases or [])))
        )
        
        # Generate insights
        insights = self._generate_insights(news, combined_sentiment)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(combined_sentiment)
        
        # Calculate impact score
        impact_score = self._calculate_impact_score(news, combined_sentiment)
        
        # Determine risk level
        risk_level = self._determine_risk_level(combined_sentiment, impact_score)
        
        # Create analysis result
        result = AnalysisResult(
            id=f"sentiment_{news.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            analysis_type=AnalysisType.SENTIMENT_ANALYSIS,
            subject_id=news.id,
            sentiment_score=combined_sentiment,
            impact_score=impact_score,
            confidence_level=combined_confidence,
            summary=self._generate_summary(news, combined_sentiment),
            key_insights=insights,
            recommendations=recommendations,
            risk_level=risk_level,
            analysis_method="Financial Sentiment Analysis",
            data_sources=[news.source.value],
            created_at=datetime.now(),
            analyst="AI_Sentiment_Analyzer",
            metadata={"news_category": news.category.value}
        )
        
        return result
    
    def _generate_insights(self, news: FinancialNews, sentiment: SentimentScore) -> List[str]:
        """Generate insights based on sentiment analysis"""
        insights = []
        
        if sentiment.is_reliable:
            insights.append(f"High confidence {sentiment.sentiment_type.value.replace('_', ' ')} sentiment detected")
        
        if sentiment.key_phrases:
            insights.append(f"Key indicators: {', '.join(sentiment.key_phrases[:5])}")
        
        if news.mentioned_symbols:
            insights.append(f"Analysis covers symbols: {', '.join(news.mentioned_symbols)}")
        
        # Category-specific insights
        if news.category.value == "earnings":
            insights.append("Earnings-related sentiment may have immediate market impact")
        elif news.category.value == "economic_indicators":
            insights.append("Economic indicator sentiment affects broader market trends")
        
        return insights
    
    def _generate_recommendations(self, sentiment: SentimentScore) -> List[str]:
        """Generate recommendations based on sentiment"""
        recommendations = []
        
        if sentiment.sentiment_type == SentimentType.VERY_POSITIVE:
            recommendations.append("Consider monitoring for potential buying opportunities")
            recommendations.append("Watch for sustained positive momentum")
        elif sentiment.sentiment_type == SentimentType.VERY_NEGATIVE:
            recommendations.append("Exercise caution and consider risk management")
            recommendations.append("Monitor for potential market overreaction")
        elif sentiment.sentiment_type == SentimentType.NEUTRAL:
            recommendations.append("Continue monitoring for trend development")
            recommendations.append("Look for additional confirming signals")
        
        if not sentiment.is_reliable:
            recommendations.append("Seek additional information sources for confirmation")
        
        return recommendations
    
    def _calculate_impact_score(self, news: FinancialNews, sentiment: SentimentScore) -> float:
        """Calculate potential market impact score"""
        impact = abs(sentiment.score) * sentiment.confidence
        
        # Boost impact for certain categories
        category_multipliers = {
            "earnings": 1.2,
            "economic_indicators": 1.3,
            "regulatory": 1.1,
            "market_analysis": 1.0
        }
        
        multiplier = category_multipliers.get(news.category.value, 1.0)
        
        # Boost for high-profile sources
        source_multipliers = {
            "bloomberg": 1.1,
            "reuters": 1.1,
            "wall_street_journal": 1.05
        }
        
        source_multiplier = source_multipliers.get(news.source.value, 1.0)
        
        return min(impact * multiplier * source_multiplier, 1.0)
    
    def _determine_risk_level(self, sentiment: SentimentScore, impact_score: float) -> str:
        """Determine risk level based on sentiment and impact"""
        if impact_score > 0.7 and abs(sentiment.score) > 0.6:
            return "high"
        elif impact_score > 0.4 or abs(sentiment.score) > 0.3:
            return "medium"
        else:
            return "low"
    
    def _generate_summary(self, news: FinancialNews, sentiment: SentimentScore) -> str:
        """Generate analysis summary"""
        sentiment_desc = sentiment.sentiment_type.value.replace('_', ' ')
        confidence_desc = "high" if sentiment.is_reliable else "moderate"
        
        return (f"Sentiment analysis of {news.source.value} article reveals "
                f"{sentiment_desc} sentiment with {confidence_desc} confidence. "
                f"Analysis covers {news.category.value.replace('_', ' ')} category.")
    
    def set_analyzer(self, analyzer: ISentimentAnalyzer):
        """Change the sentiment analyzer"""
        self._analyzer = analyzer
    
    def get_analyzer_info(self) -> Dict[str, Any]:
        """Get information about current analyzer"""
        return {
            "analyzer_type": type(self._analyzer).__name__,
            "capabilities": ["text_analysis", "batch_analysis", "financial_focus"]
        }
