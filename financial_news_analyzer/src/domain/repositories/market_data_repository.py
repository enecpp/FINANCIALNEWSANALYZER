"""
Market Data Repository Interface
Abstract interface for market data access
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..entities.market_data import MarketData, Stock, MarketType
from ..entities.market import Market

class IMarketDataRepository(ABC):
    """
    Interface for market data access operations
    
    SOLID Principles:
    - Interface Segregation: Clean, focused interface for market data
    - Dependency Inversion: Abstract data access layer
    - Single Responsibility: Only defines market data access contract
    """
    
    @abstractmethod
    def get_market_data(self, market_type: MarketType, limit: int = 100) -> Optional[MarketData]:
        """
        Get current market data
        
        Args:
            market_type: Type of market to retrieve
            limit: Maximum number of stocks to include
            
        Returns:
            Market data if available, None otherwise
        """
        pass
    
    @abstractmethod
    def get_stock_by_symbol(self, symbol: str) -> Optional[Stock]:
        """
        Get stock data by symbol
        
        Args:
            symbol: Stock symbol to lookup
            
        Returns:
            Stock data if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_stocks_by_exchange(self, exchange: str, limit: int = 100) -> List[Stock]:
        """
        Get stocks by exchange
        
        Args:
            exchange: Exchange identifier
            limit: Maximum number of stocks
            
        Returns:
            List of stocks from the exchange
        """
        pass
    
    @abstractmethod
    def get_top_gainers(self, limit: int = 10) -> List[Stock]:
        """
        Get top gaining stocks
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of top gaining stocks
        """
        pass
    
    @abstractmethod
    def get_top_losers(self, limit: int = 10) -> List[Stock]:
        """
        Get top losing stocks
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of top losing stocks
        """
        pass
    
    @abstractmethod
    def get_most_active(self, limit: int = 10) -> List[Stock]:
        """
        Get most active stocks by volume
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of most active stocks
        """
        pass
    
    @abstractmethod
    def search_stocks(self, query: str, limit: int = 20) -> List[Stock]:
        """
        Search stocks by name or symbol
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching stocks
        """
        pass
    
    @abstractmethod
    def get_market_overview(self) -> Dict[str, Any]:
        """
        Get overall market overview
        
        Returns:
            Dictionary with market overview data
        """
        pass
    
    @abstractmethod
    def get_sector_performance(self) -> Dict[str, float]:
        """
        Get performance by sector
        
        Returns:
            Dictionary mapping sectors to performance percentages
        """
        pass
    
    @abstractmethod
    def get_market_indices(self) -> List[Stock]:
        """
        Get major market indices
        
        Returns:
            List of market index data
        """
        pass
    
    @abstractmethod
    def save_market_data(self, market_data: MarketData) -> bool:
        """
        Save market data snapshot
        
        Args:
            market_data: Market data to save
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_historical_data(self, symbol: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Get historical data for a symbol
        
        Args:
            symbol: Stock symbol
            days_back: Number of days of history
            
        Returns:
            List of historical data points
        """
        pass
    
    @abstractmethod
    def get_market_status(self) -> Dict[str, Any]:
        """
        Get current market status information
        
        Returns:
            Dictionary with market status data
        """
        pass
