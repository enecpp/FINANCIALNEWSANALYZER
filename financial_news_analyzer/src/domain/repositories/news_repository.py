"""
News Repository Interface
Abstract interface for news data access
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..entities.financial_news import FinancialNews, NewsCategory, NewsSource

class INewsRepository(ABC):
    """
    Interface for news data access operations
    
    SOLID Principles:
    - Interface Segregation: Clean, focused interface
    - Dependency Inversion: Abstract data access
    - Single Responsibility: Only defines data access contract
    """
    
    @abstractmethod
    def save(self, news: FinancialNews) -> bool:
        """
        Save a news article
        
        Args:
            news: News article to save
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def find_by_id(self, news_id: str) -> Optional[FinancialNews]:
        """
        Find news by ID
        
        Args:
            news_id: Unique identifier for the news
            
        Returns:
            News article if found, None otherwise
        """
        pass
    
    @abstractmethod
    def find_by_criteria(self, criteria) -> List[FinancialNews]:
        """
        Find news by search criteria
        
        Args:
            criteria: Search criteria object
            
        Returns:
            List of matching news articles
        """
        pass
    
    @abstractmethod
    def find_by_symbol(self, symbol: str, limit: int = 50) -> List[FinancialNews]:
        """
        Find news mentioning specific stock symbol
        
        Args:
            symbol: Stock symbol to search for
            limit: Maximum number of results
            
        Returns:
            List of news articles mentioning the symbol
        """
        pass
    
    @abstractmethod
    def find_by_category(self, category: NewsCategory, limit: int = 50) -> List[FinancialNews]:
        """
        Find news by category
        
        Args:
            category: News category to filter by
            limit: Maximum number of results
            
        Returns:
            List of news articles in the category
        """
        pass
    
    @abstractmethod
    def find_by_source(self, source: NewsSource, limit: int = 50) -> List[FinancialNews]:
        """
        Find news by source
        
        Args:
            source: News source to filter by
            limit: Maximum number of results
            
        Returns:
            List of news articles from the source
        """
        pass
    
    @abstractmethod
    def find_recent(self, hours_back: int = 24, limit: int = 50) -> List[FinancialNews]:
        """
        Find recent news within specified time window
        
        Args:
            hours_back: Hours to look back from now
            limit: Maximum number of results
            
        Returns:
            List of recent news articles
        """
        pass
    
    @abstractmethod
    def find_by_sentiment_range(self, min_score: float, max_score: float, 
                               limit: int = 50) -> List[FinancialNews]:
        """
        Find news by sentiment score range
        
        Args:
            min_score: Minimum sentiment score (-1.0 to 1.0)
            max_score: Maximum sentiment score (-1.0 to 1.0)
            limit: Maximum number of results
            
        Returns:
            List of news articles within sentiment range
        """
        pass
    
    @abstractmethod
    def find_high_impact(self, min_impact: float = 0.7, limit: int = 50) -> List[FinancialNews]:
        """
        Find high-impact news articles
        
        Args:
            min_impact: Minimum impact score threshold
            limit: Maximum number of results
            
        Returns:
            List of high-impact news articles
        """
        pass
    
    @abstractmethod
    def update(self, news: FinancialNews) -> bool:
        """
        Update existing news article
        
        Args:
            news: Updated news article
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, news_id: str) -> bool:
        """
        Delete news article by ID
        
        Args:
            news_id: ID of news to delete
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def count_by_criteria(self, criteria) -> int:
        """
        Count news articles matching criteria
        
        Args:
            criteria: Search criteria object
            
        Returns:
            Number of matching articles
        """
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get repository statistics
        
        Returns:
            Dictionary with statistics about the news data
        """
        pass
