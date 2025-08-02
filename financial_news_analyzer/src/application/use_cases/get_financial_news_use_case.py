"""
Get Financial News Use Case
Handles retrieval and filtering of financial news
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

from ...domain.entities.financial_news import FinancialNews, NewsCategory, NewsSource
from ...domain.repositories.news_repository import INewsRepository

@dataclass
class NewsSearchCriteria:
    """
    Search criteria for financial news
    
    Clean Code Principles:
    - Value Object pattern for complex parameters
    - Immutable data structure
    - Clear validation rules
    """
    
    # Time filters
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    hours_back: Optional[int] = 24
    
    # Content filters
    keywords: Optional[List[str]] = None
    symbols: Optional[List[str]] = None
    categories: Optional[List[NewsCategory]] = None
    sources: Optional[List[NewsSource]] = None
    
    # Sentiment filters
    min_sentiment_score: Optional[float] = None
    max_sentiment_score: Optional[float] = None
    min_confidence: Optional[float] = None
    
    # Impact filters
    min_impact_score: Optional[float] = None
    high_impact_only: bool = False
    
    # Pagination
    limit: int = 50
    offset: int = 0
    
    # Sorting
    sort_by: str = "published_at"  # published_at, sentiment_score, impact_score
    sort_order: str = "desc"  # desc, asc
    
    def __post_init__(self):
        """Validate and normalize criteria"""
        # Set default time range if not specified
        if not self.start_date and not self.end_date and self.hours_back:
            self.end_date = datetime.now()
            self.start_date = self.end_date - timedelta(hours=self.hours_back)
        
        # Validate sentiment score ranges
        if self.min_sentiment_score is not None:
            self.min_sentiment_score = max(-1.0, min(1.0, self.min_sentiment_score))
        
        if self.max_sentiment_score is not None:
            self.max_sentiment_score = max(-1.0, min(1.0, self.max_sentiment_score))
        
        # Validate confidence range
        if self.min_confidence is not None:
            self.min_confidence = max(0.0, min(1.0, self.min_confidence))
        
        # Validate impact score range
        if self.min_impact_score is not None:
            self.min_impact_score = max(0.0, min(1.0, self.min_impact_score))
        
        # Validate pagination
        self.limit = max(1, min(1000, self.limit))
        self.offset = max(0, self.offset)
        
        # Validate sorting
        valid_sort_fields = {"published_at", "sentiment_score", "impact_score", "confidence_score"}
        if self.sort_by not in valid_sort_fields:
            self.sort_by = "published_at"
        
        if self.sort_order not in {"desc", "asc"}:
            self.sort_order = "desc"

class GetFinancialNewsUseCase:
    """
    Use case for retrieving financial news with various filters
    
    SOLID Principles:
    - Single Responsibility: Handles news retrieval logic only
    - Open/Closed: Extensible for new search criteria
    - Dependency Inversion: Depends on repository abstraction
    """
    
    def __init__(self, news_repository: INewsRepository):
        """Initialize with news repository dependency"""
        self._news_repository = news_repository
    
    def execute(self, criteria: NewsSearchCriteria) -> Dict[str, Any]:
        """
        Execute the use case to retrieve financial news
        
        Args:
            criteria: Search criteria for filtering news
            
        Returns:
            Dictionary containing news results and metadata
        """
        try:
            # Retrieve news from repository
            news_list = self._news_repository.find_by_criteria(criteria)
            
            # Apply additional filtering if needed
            filtered_news = self._apply_advanced_filters(news_list, criteria)
            
            # Sort results
            sorted_news = self._sort_news(filtered_news, criteria.sort_by, criteria.sort_order)
            
            # Apply pagination
            paginated_news = self._paginate_results(sorted_news, criteria.limit, criteria.offset)
            
            # Generate metadata
            metadata = self._generate_metadata(news_list, filtered_news, paginated_news, criteria)
            
            return {
                "news": [news.to_dict() for news in paginated_news],
                "metadata": metadata,
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "news": [],
                "metadata": {"error": str(e)},
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_trending_news(self, hours_back: int = 6, limit: int = 10) -> List[FinancialNews]:
        """
        Get trending news based on recent activity and sentiment
        
        Args:
            hours_back: Hours to look back for trending analysis
            limit: Maximum number of trending articles
            
        Returns:
            List of trending news articles
        """
        criteria = NewsSearchCriteria(
            hours_back=hours_back,
            limit=limit * 3,  # Get more to filter from
            sort_by="impact_score",
            sort_order="desc"
        )
        
        result = self.execute(criteria)
        
        if not result["success"]:
            return []
        
        # Convert back to entities for trending analysis
        news_list = [FinancialNews.from_dict(news_dict) for news_dict in result["news"]]
        
        # Apply trending logic
        trending_news = self._calculate_trending_score(news_list)
        
        return trending_news[:limit]
    
    def get_news_by_symbol(self, symbol: str, hours_back: int = 24) -> List[FinancialNews]:
        """
        Get news mentioning specific stock symbol
        
        Args:
            symbol: Stock symbol to search for
            hours_back: Hours to look back
            
        Returns:
            List of news mentioning the symbol
        """
        criteria = NewsSearchCriteria(
            symbols=[symbol.upper()],
            hours_back=hours_back,
            sort_by="published_at",
            sort_order="desc"
        )
        
        result = self.execute(criteria)
        
        if not result["success"]:
            return []
        
        return [FinancialNews.from_dict(news_dict) for news_dict in result["news"]]
    
    def get_high_impact_news(self, min_impact: float = 0.7, hours_back: int = 12) -> List[FinancialNews]:
        """
        Get high-impact news articles
        
        Args:
            min_impact: Minimum impact score threshold
            hours_back: Hours to look back
            
        Returns:
            List of high-impact news articles
        """
        criteria = NewsSearchCriteria(
            min_impact_score=min_impact,
            hours_back=hours_back,
            sort_by="impact_score",
            sort_order="desc"
        )
        
        result = self.execute(criteria)
        
        if not result["success"]:
            return []
        
        return [FinancialNews.from_dict(news_dict) for news_dict in result["news"]]
    
    def get_news_summary(self, criteria: NewsSearchCriteria) -> Dict[str, Any]:
        """
        Get summarized view of news matching criteria
        
        Args:
            criteria: Search criteria
            
        Returns:
            Summary statistics and insights
        """
        result = self.execute(criteria)
        
        if not result["success"]:
            return {"error": "Failed to retrieve news"}
        
        news_list = [FinancialNews.from_dict(news_dict) for news_dict in result["news"]]
        
        return self._generate_news_summary(news_list)
    
    def _apply_advanced_filters(self, news_list: List[FinancialNews], 
                              criteria: NewsSearchCriteria) -> List[FinancialNews]:
        """Apply additional filtering logic not handled by repository"""
        filtered = news_list
        
        # High impact filter
        if criteria.high_impact_only:
            filtered = [news for news in filtered if news.is_high_impact]
        
        # Confidence filter
        if criteria.min_confidence is not None:
            filtered = [news for news in filtered 
                       if news.confidence_score is not None and 
                       news.confidence_score >= criteria.min_confidence]
        
        return filtered
    
    def _sort_news(self, news_list: List[FinancialNews], sort_by: str, sort_order: str) -> List[FinancialNews]:
        """Sort news list by specified criteria"""
        reverse = (sort_order == "desc")
        
        if sort_by == "published_at":
            return sorted(news_list, key=lambda x: x.published_at, reverse=reverse)
        elif sort_by == "sentiment_score":
            return sorted(news_list, 
                         key=lambda x: x.sentiment_score or 0.0, 
                         reverse=reverse)
        elif sort_by == "impact_score":
            return sorted(news_list, 
                         key=lambda x: x.impact_score or 0.0, 
                         reverse=reverse)
        elif sort_by == "confidence_score":
            return sorted(news_list, 
                         key=lambda x: x.confidence_score or 0.0, 
                         reverse=reverse)
        else:
            return news_list
    
    def _paginate_results(self, news_list: List[FinancialNews], 
                         limit: int, offset: int) -> List[FinancialNews]:
        """Apply pagination to results"""
        return news_list[offset:offset + limit]
    
    def _generate_metadata(self, original_list: List[FinancialNews],
                          filtered_list: List[FinancialNews],
                          paginated_list: List[FinancialNews],
                          criteria: NewsSearchCriteria) -> Dict[str, Any]:
        """Generate metadata about the search results"""
        return {
            "total_found": len(original_list),
            "total_after_filtering": len(filtered_list),
            "returned_count": len(paginated_list),
            "offset": criteria.offset,
            "limit": criteria.limit,
            "has_more": (criteria.offset + len(paginated_list)) < len(filtered_list),
            "search_criteria": {
                "time_range": f"{criteria.start_date} to {criteria.end_date}" if criteria.start_date else None,
                "categories": [cat.value for cat in criteria.categories] if criteria.categories else None,
                "sources": [src.value for src in criteria.sources] if criteria.sources else None,
                "keywords": criteria.keywords,
                "symbols": criteria.symbols,
                "min_sentiment": criteria.min_sentiment_score,
                "min_impact": criteria.min_impact_score
            }
        }
    
    def _calculate_trending_score(self, news_list: List[FinancialNews]) -> List[FinancialNews]:
        """Calculate trending score for news articles"""
        scored_news = []
        
        for news in news_list:
            # Calculate trending score based on multiple factors
            score = 0.0
            
            # Recency factor (newer = higher score)
            hours_old = (datetime.now() - news.published_at).total_seconds() / 3600
            recency_score = max(0, 1.0 - (hours_old / 24))  # Decay over 24 hours
            score += recency_score * 0.3
            
            # Impact factor
            if news.impact_score:
                score += news.impact_score * 0.4
            
            # Sentiment strength factor
            if news.sentiment_score:
                score += abs(news.sentiment_score) * 0.2
            
            # Confidence factor
            if news.confidence_score:
                score += news.confidence_score * 0.1
            
            scored_news.append((news, score))
        
        # Sort by trending score
        scored_news.sort(key=lambda x: x[1], reverse=True)
        
        return [news for news, score in scored_news]
    
    def _generate_news_summary(self, news_list: List[FinancialNews]) -> Dict[str, Any]:
        """Generate summary statistics for news list"""
        if not news_list:
            return {"message": "No news found"}
        
        # Calculate sentiment distribution
        sentiment_scores = [news.sentiment_score for news in news_list if news.sentiment_score is not None]
        positive_count = sum(1 for score in sentiment_scores if score > 0.1)
        negative_count = sum(1 for score in sentiment_scores if score < -0.1)
        neutral_count = len(sentiment_scores) - positive_count - negative_count
        
        # Calculate category distribution
        category_counts = {}
        for news in news_list:
            category = news.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Calculate source distribution
        source_counts = {}
        for news in news_list:
            source = news.source.value
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Find most mentioned symbols
        all_symbols = []
        for news in news_list:
            if news.mentioned_symbols:
                all_symbols.extend(news.mentioned_symbols)
        
        symbol_counts = {}
        for symbol in all_symbols:
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        
        top_symbols = sorted(symbol_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_articles": len(news_list),
            "sentiment_distribution": {
                "positive": positive_count,
                "negative": negative_count,
                "neutral": neutral_count
            },
            "category_distribution": category_counts,
            "source_distribution": source_counts,
            "top_mentioned_symbols": top_symbols,
            "time_range": {
                "earliest": min(news.published_at for news in news_list).isoformat(),
                "latest": max(news.published_at for news in news_list).isoformat()
            },
            "average_sentiment": sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0,
            "high_impact_count": sum(1 for news in news_list if news.is_high_impact)
        }
