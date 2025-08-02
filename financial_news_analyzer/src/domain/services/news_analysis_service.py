"""
News Analysis Service
Comprehensive financial news analysis and processing
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import re

from ..entities.financial_news import FinancialNews, NewsCategory, NewsSource
from ..entities.analysis_result import AnalysisResult, AnalysisType
from .sentiment_analysis_service import SentimentAnalysisService

class INewsProcessor(ABC):
    """
    Interface for news processing implementations
    
    SOLID Principles:
    - Interface Segregation: Focused interface for news processing
    - Dependency Inversion: Abstracts news processing logic
    """
    
    @abstractmethod
    def extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text"""
        pass
    
    @abstractmethod
    def extract_symbols(self, text: str) -> List[str]:
        """Extract stock symbols from text"""
        pass
    
    @abstractmethod
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate summary of the text"""
        pass

class FinancialNewsProcessor(INewsProcessor):
    """
    Financial news processor with domain-specific logic
    
    Clean Code Principles:
    - Single Responsibility: Handles news text processing only
    - DRY: Reusable processing methods
    - Readable and expressive method names
    """
    
    def __init__(self):
        """Initialize with financial keywords and patterns"""
        self._financial_keywords = {
            # Market terms
            'market', 'stock', 'share', 'equity', 'bond', 'commodity', 'forex',
            'trading', 'investor', 'investment', 'portfolio', 'asset', 'security',
            
            # Financial metrics
            'revenue', 'profit', 'earnings', 'ebitda', 'margin', 'growth', 'yield',
            'dividend', 'valuation', 'pe ratio', 'market cap', 'volume', 'volatility',
            
            # Corporate actions
            'merger', 'acquisition', 'ipo', 'buyback', 'split', 'dividend', 'spinoff',
            'bankruptcy', 'restructuring', 'delisting', 'listing',
            
            # Economic indicators
            'gdp', 'inflation', 'unemployment', 'fed', 'interest rate', 'monetary policy',
            'fiscal policy', 'central bank', 'recession', 'recovery', 'stimulus',
            
            # Market movements
            'bull', 'bear', 'rally', 'correction', 'crash', 'bubble', 'support',
            'resistance', 'breakout', 'trend', 'momentum', 'oversold', 'overbought'
        }
        
        # Common stock symbol patterns
        self._symbol_patterns = [
            r'\b[A-Z]{1,5}\b',  # 1-5 letter symbols
            r'\$[A-Z]{1,5}\b',  # Symbols with $ prefix
            r'\b[A-Z]{1,5}:[A-Z]{2,4}\b',  # Exchange:Symbol format
        ]
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract financial keywords from text
        
        Args:
            text: Text to process
            
        Returns:
            List of relevant financial keywords
        """
        if not text:
            return []
        
        text_lower = text.lower()
        found_keywords = []
        
        # Find direct keyword matches
        for keyword in self._financial_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        # Extract additional terms using NLP-like approach
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Financial suffixes and prefixes
        financial_patterns = [
            r'\w*price\w*', r'\w*cost\w*', r'\w*value\w*', r'\w*rate\w*',
            r'\w*index\w*', r'\w*fund\w*', r'\w*corp\w*', r'\w*inc\w*'
        ]
        
        for pattern in financial_patterns:
            matches = re.findall(pattern, text_lower)
            found_keywords.extend(matches)
        
        # Remove duplicates and sort
        return sorted(list(set(found_keywords)))
    
    def extract_symbols(self, text: str) -> List[str]:
        """
        Extract stock symbols from text
        
        Args:
            text: Text to process
            
        Returns:
            List of potential stock symbols
        """
        if not text:
            return []
        
        symbols = []
        
        for pattern in self._symbol_patterns:
            matches = re.findall(pattern, text)
            symbols.extend(matches)
        
        # Clean up symbols
        cleaned_symbols = []
        for symbol in symbols:
            # Remove $ prefix if present
            clean_symbol = symbol.replace('$', '').strip()
            
            # Filter out common false positives
            false_positives = {
                'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
                'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'USE',
                'MAN', 'NEW', 'NOW', 'OLD', 'SEE', 'HIM', 'TWO', 'HOW', 'ITS',
                'WHO', 'OIL', 'GAS', 'CEO', 'CFO', 'IPO', 'SEC', 'FAQ', 'API'
            }
            
            if (clean_symbol and 
                len(clean_symbol) >= 1 and 
                len(clean_symbol) <= 5 and 
                clean_symbol not in false_positives):
                cleaned_symbols.append(clean_symbol)
        
        return sorted(list(set(cleaned_symbols)))
    
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """
        Generate summary of financial text
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
            
        Returns:
            Generated summary
        """
        if not text or len(text) <= max_length:
            return text
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return text[:max_length] + "..."
        
        # Score sentences based on financial relevance
        scored_sentences = []
        for sentence in sentences:
            score = self._score_sentence_relevance(sentence)
            scored_sentences.append((sentence, score))
        
        # Sort by relevance score
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        # Build summary
        summary = ""
        for sentence, score in scored_sentences:
            if len(summary) + len(sentence) + 2 <= max_length:
                if summary:
                    summary += ". "
                summary += sentence
            else:
                break
        
        return summary or text[:max_length] + "..."
    
    def _score_sentence_relevance(self, sentence: str) -> float:
        """Score sentence relevance for financial analysis"""
        if not sentence:
            return 0.0
        
        sentence_lower = sentence.lower()
        score = 0.0
        
        # Count financial keywords
        for keyword in self._financial_keywords:
            if keyword in sentence_lower:
                score += 1.0
        
        # Boost for numbers (often important in financial context)
        numbers = re.findall(r'\d+', sentence)
        score += len(numbers) * 0.5
        
        # Boost for currency symbols
        currency_symbols = re.findall(r'[\$€£¥]', sentence)
        score += len(currency_symbols) * 0.3
        
        # Penalty for very long sentences (harder to understand)
        if len(sentence) > 100:
            score *= 0.8
        
        return score

class NewsAnalysisService:
    """
    Service for comprehensive news analysis
    
    Design Patterns:
    - Strategy Pattern: Configurable processing strategies
    - Observer Pattern: Notify about analysis completion
    - Command Pattern: Encapsulate analysis operations
    """
    
    def __init__(self, 
                 processor: Optional[INewsProcessor] = None,
                 sentiment_service: Optional[SentimentAnalysisService] = None):
        """Initialize service with dependencies"""
        self._processor = processor or FinancialNewsProcessor()
        self._sentiment_service = sentiment_service or SentimentAnalysisService()
    
    def analyze_news_article(self, news: FinancialNews) -> AnalysisResult:
        """
        Perform comprehensive analysis on a news article
        
        Args:
            news: News article to analyze
            
        Returns:
            Complete analysis result
        """
        # Extract keywords and symbols
        keywords = self._processor.extract_keywords(news.content)
        symbols = self._processor.extract_symbols(news.content)
        
        # Generate summary if not present
        summary = news.summary or self._processor.generate_summary(news.content)
        
        # Update news with extracted information
        news.keywords = keywords[:20]  # Top 20 keywords
        news.mentioned_symbols = symbols[:10]  # Top 10 symbols
        if not news.summary:
            news.summary = summary
        
        # Perform sentiment analysis
        sentiment_result = self._sentiment_service.analyze_news(news)
        
        # Calculate additional metrics
        impact_score = self._calculate_news_impact(news, sentiment_result)
        relevance_score = self._calculate_relevance_score(news)
        
        # Generate insights
        insights = self._generate_comprehensive_insights(news, sentiment_result)
        
        # Generate recommendations
        recommendations = self._generate_trading_recommendations(news, sentiment_result)
        
        # Create comprehensive analysis result
        analysis_result = AnalysisResult(
            id=f"news_analysis_{news.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            analysis_type=AnalysisType.NEWS_IMPACT_ANALYSIS,
            subject_id=news.id,
            sentiment_score=sentiment_result.sentiment_score,
            impact_score=impact_score,
            confidence_level=sentiment_result.confidence_level,
            summary=f"Comprehensive analysis of {news.source.value} article on {news.category.value}",
            key_insights=insights,
            recommendations=recommendations,
            risk_level=self._assess_risk_level(news, sentiment_result, impact_score),
            analysis_method="Multi-factor News Analysis",
            data_sources=[news.source.value],
            processing_time_ms=None,  # Could be measured
            created_at=datetime.now(),
            analyst="AI_News_Analyzer",
            metadata={
                "news_category": news.category.value,
                "keywords_count": len(keywords),
                "symbols_count": len(symbols),
                "relevance_score": relevance_score,
                "article_length": len(news.content),
                "published_hours_ago": (datetime.now() - news.published_at).total_seconds() / 3600
            }
        )
        
        return analysis_result
    
    def analyze_news_batch(self, news_list: List[FinancialNews]) -> List[AnalysisResult]:
        """Analyze multiple news articles efficiently"""
        return [self.analyze_news_article(news) for news in news_list]
    
    def find_trending_topics(self, news_list: List[FinancialNews], 
                           time_window_hours: int = 24) -> Dict[str, Any]:
        """
        Find trending topics from news articles
        
        Args:
            news_list: List of news articles
            time_window_hours: Time window for trend analysis
            
        Returns:
            Dictionary with trending analysis
        """
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        recent_news = [n for n in news_list if n.published_at >= cutoff_time]
        
        if not recent_news:
            return {"trending_keywords": [], "trending_symbols": [], "sentiment_trend": "neutral"}
        
        # Aggregate keywords
        all_keywords = []
        all_symbols = []
        sentiment_scores = []
        
        for news in recent_news:
            if news.keywords:
                all_keywords.extend(news.keywords)
            if news.mentioned_symbols:
                all_symbols.extend(news.mentioned_symbols)
            if news.sentiment_score:
                sentiment_scores.append(news.sentiment_score)
        
        # Count occurrences
        keyword_counts = {}
        for keyword in all_keywords:
            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        symbol_counts = {}
        for symbol in all_symbols:
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        
        # Get top trending items
        trending_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        trending_symbols = sorted(symbol_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Calculate overall sentiment trend
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        sentiment_trend = "positive" if avg_sentiment > 0.1 else "negative" if avg_sentiment < -0.1 else "neutral"
        
        return {
            "trending_keywords": trending_keywords,
            "trending_symbols": trending_symbols,
            "sentiment_trend": sentiment_trend,
            "average_sentiment": avg_sentiment,
            "news_count": len(recent_news),
            "time_window": f"{time_window_hours} hours"
        }
    
    def _calculate_news_impact(self, news: FinancialNews, sentiment_result: AnalysisResult) -> float:
        """Calculate potential market impact of news"""
        base_impact = sentiment_result.impact_score or 0.5
        
        # Category impact multipliers
        category_impact = {
            NewsCategory.EARNINGS: 1.3,
            NewsCategory.ECONOMIC_INDICATORS: 1.2,
            NewsCategory.REGULATORY: 1.1,
            NewsCategory.MARKET_ANALYSIS: 1.0,
            NewsCategory.CORPORATE_NEWS: 0.9,
            NewsCategory.GLOBAL_MARKETS: 0.8
        }
        
        # Source credibility multipliers
        source_impact = {
            NewsSource.BLOOMBERG: 1.2,
            NewsSource.REUTERS: 1.2,
            NewsSource.WALL_STREET_JOURNAL: 1.1,
            NewsSource.FINANCIAL_TIMES: 1.1,
            NewsSource.CNBC: 1.0,
            NewsSource.YAHOO_FINANCE: 0.9,
            NewsSource.MARKETWATCH: 0.9
        }
        
        # Time decay (newer news has higher impact)
        hours_old = (datetime.now() - news.published_at).total_seconds() / 3600
        time_decay = max(0.5, 1.0 - (hours_old / 48))  # Decay over 48 hours
        
        # Calculate final impact
        final_impact = (
            base_impact * 
            category_impact.get(news.category, 1.0) * 
            source_impact.get(news.source, 1.0) * 
            time_decay
        )
        
        return min(final_impact, 1.0)
    
    def _calculate_relevance_score(self, news: FinancialNews) -> float:
        """Calculate how relevant the news is to financial markets"""
        score = 0.5  # Base score
        
        # Boost for financial keywords
        if news.keywords:
            score += min(len(news.keywords) * 0.02, 0.3)
        
        # Boost for mentioned symbols
        if news.mentioned_symbols:
            score += min(len(news.mentioned_symbols) * 0.05, 0.2)
        
        # Category relevance
        category_relevance = {
            NewsCategory.MARKET_ANALYSIS: 1.0,
            NewsCategory.EARNINGS: 0.9,
            NewsCategory.ECONOMIC_INDICATORS: 0.8,
            NewsCategory.CORPORATE_NEWS: 0.7,
            NewsCategory.REGULATORY: 0.6,
            NewsCategory.GLOBAL_MARKETS: 0.5
        }
        
        score *= category_relevance.get(news.category, 0.5)
        
        return min(score, 1.0)
    
    def _generate_comprehensive_insights(self, news: FinancialNews, 
                                       sentiment_result: AnalysisResult) -> List[str]:
        """Generate comprehensive insights about the news"""
        insights = []
        
        # Basic sentiment insight
        sentiment_score = sentiment_result.sentiment_score
        if sentiment_score:
            insights.append(
                f"Article sentiment: {sentiment_score.sentiment_emoji} "
                f"{sentiment_score.sentiment_type.value.replace('_', ' ').title()} "
                f"(confidence: {sentiment_score.confidence:.1%})"
            )
        
        # Symbol insights
        if news.mentioned_symbols:
            insights.append(f"Mentioned securities: {', '.join(news.mentioned_symbols[:5])}")
        
        # Keyword insights
        if news.keywords:
            top_keywords = [kw for kw in news.keywords[:5] if len(kw) > 3]
            if top_keywords:
                insights.append(f"Key themes: {', '.join(top_keywords)}")
        
        # Timing insights
        hours_old = (datetime.now() - news.published_at).total_seconds() / 3600
        if hours_old < 1:
            insights.append("🔥 Breaking news - immediate market relevance")
        elif hours_old < 6:
            insights.append("📈 Recent news - high current relevance")
        elif hours_old > 24:
            insights.append("📰 Older news - limited immediate impact")
        
        # Category-specific insights
        if news.category == NewsCategory.EARNINGS:
            insights.append("💰 Earnings news may trigger volatility in mentioned stocks")
        elif news.category == NewsCategory.ECONOMIC_INDICATORS:
            insights.append("📊 Economic indicator may influence broader market sentiment")
        elif news.category == NewsCategory.REGULATORY:
            insights.append("⚖️ Regulatory news may have sector-wide implications")
        
        return insights
    
    def _generate_trading_recommendations(self, news: FinancialNews, 
                                        sentiment_result: AnalysisResult) -> List[str]:
        """Generate trading-focused recommendations"""
        recommendations = []
        
        sentiment_score = sentiment_result.sentiment_score
        impact_score = sentiment_result.impact_score or 0.5
        
        if not sentiment_score:
            recommendations.append("🔍 Insufficient sentiment data - gather more information")
            return recommendations
        
        # High impact recommendations
        if impact_score > 0.7:
            if sentiment_score.score > 0.3:
                recommendations.append("📈 High positive impact expected - consider long positions")
                recommendations.append("⏰ Monitor for entry opportunities during dips")
            elif sentiment_score.score < -0.3:
                recommendations.append("📉 High negative impact expected - consider protective measures")
                recommendations.append("🛡️ Review stop-loss levels for affected positions")
        
        # Medium impact recommendations
        elif impact_score > 0.4:
            recommendations.append("👀 Moderate impact expected - monitor closely")
            recommendations.append("⚖️ Consider position sizing adjustments")
        
        # Symbol-specific recommendations
        if news.mentioned_symbols:
            recommendations.append(f"🎯 Focus monitoring on: {', '.join(news.mentioned_symbols[:3])}")
        
        # Risk management
        if not sentiment_score.is_reliable:
            recommendations.append("⚠️ Low confidence analysis - use additional confirmation")
        
        # Timing recommendations
        hours_old = (datetime.now() - news.published_at).total_seconds() / 3600
        if hours_old < 2:
            recommendations.append("⚡ Fresh news - immediate market reaction possible")
        
        return recommendations
    
    def _assess_risk_level(self, news: FinancialNews, sentiment_result: AnalysisResult, 
                          impact_score: float) -> str:
        """Assess overall risk level"""
        sentiment_score = sentiment_result.sentiment_score
        
        # High risk conditions
        if (impact_score > 0.7 and 
            sentiment_score and 
            abs(sentiment_score.score) > 0.6):
            return "high"
        
        # Medium risk conditions
        if (impact_score > 0.4 or 
            (sentiment_score and abs(sentiment_score.score) > 0.3)):
            return "medium"
        
        return "low"
