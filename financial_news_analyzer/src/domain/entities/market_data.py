"""
Market Data Entities
Represents market data, stocks, and financial metrics
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from decimal import Decimal

class MarketType(Enum):
    """Types of financial markets"""
    STOCK = "stock"
    FOREX = "forex"
    CRYPTO = "crypto"
    COMMODITY = "commodity"
    BOND = "bond"
    INDEX = "index"

class Currency(Enum):
    """Supported currencies"""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CNY = "CNY"
    CAD = "CAD"
    AUD = "AUD"
    CHF = "CHF"
    TRY = "TRY"

@dataclass
class Stock:
    """
    Represents a stock/security with current market data
    
    Clean Code Principles:
    - Meaningful names for all properties
    - Single responsibility for stock data
    - Immutable where possible
    """
    
    # Identifiers
    symbol: str
    name: str
    exchange: str
    
    # Pricing
    current_price: Decimal
    currency: Currency
    
    # Market data
    open_price: Optional[Decimal] = None
    high_price: Optional[Decimal] = None
    low_price: Optional[Decimal] = None
    previous_close: Optional[Decimal] = None
    
    # Volume and trading
    volume: Optional[int] = None
    average_volume: Optional[int] = None
    market_cap: Optional[Decimal] = None
    
    # Performance metrics
    change_amount: Optional[Decimal] = None
    change_percent: Optional[float] = None
    
    # Timestamps
    last_updated: Optional[datetime] = None
    
    # Additional data
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize computed fields"""
        if self.last_updated is None:
            self.last_updated = datetime.now()
        
        if self.metadata is None:
            self.metadata = {}
        
        # Calculate change if not provided
        if self.change_amount is None and self.previous_close is not None:
            self.change_amount = self.current_price - self.previous_close
        
        if self.change_percent is None and self.previous_close is not None and self.previous_close != 0:
            self.change_percent = float((self.current_price - self.previous_close) / self.previous_close * 100)
    
    @property
    def is_gaining(self) -> bool:
        """Check if stock is gaining value"""
        return self.change_amount is not None and self.change_amount > 0
    
    @property
    def is_losing(self) -> bool:
        """Check if stock is losing value"""
        return self.change_amount is not None and self.change_amount < 0
    
    @property
    def is_stable(self) -> bool:
        """Check if stock price is stable"""
        return self.change_amount is not None and self.change_amount == 0
    
    @property
    def performance_label(self) -> str:
        """Get performance label"""
        if self.is_gaining:
            return "📈 Gaining"
        elif self.is_losing:
            return "📉 Losing"
        else:
            return "➡️ Stable"
    
    def get_formatted_price(self) -> str:
        """Get formatted price with currency"""
        return f"{self.currency.value} {self.current_price:.2f}"
    
    def get_formatted_change(self) -> str:
        """Get formatted change amount and percentage"""
        if self.change_amount is None or self.change_percent is None:
            return "N/A"
        
        sign = "+" if self.change_amount >= 0 else ""
        return f"{sign}{self.change_amount:.2f} ({sign}{self.change_percent:.2f}%)"

@dataclass
class MarketMetrics:
    """
    Aggregated market metrics and indicators
    """
    
    # Market overview
    total_stocks: int
    gaining_stocks: int
    losing_stocks: int
    unchanged_stocks: int
    
    # Volume metrics
    total_volume: Optional[int] = None
    average_volume: Optional[int] = None
    
    # Performance metrics
    average_change_percent: Optional[float] = None
    market_sentiment_score: Optional[float] = None  # -1.0 to 1.0
    
    # Volatility
    volatility_index: Optional[float] = None
    
    # Timestamps
    calculated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize computed fields"""
        if self.calculated_at is None:
            self.calculated_at = datetime.now()
    
    @property
    def gaining_percentage(self) -> float:
        """Percentage of stocks that are gaining"""
        if self.total_stocks == 0:
            return 0.0
        return (self.gaining_stocks / self.total_stocks) * 100
    
    @property
    def losing_percentage(self) -> float:
        """Percentage of stocks that are losing"""
        if self.total_stocks == 0:
            return 0.0
        return (self.losing_stocks / self.total_stocks) * 100
    
    @property
    def market_sentiment_label(self) -> str:
        """Get market sentiment label"""
        if self.market_sentiment_score is None:
            return "Unknown"
        
        if self.market_sentiment_score > 0.3:
            return "🟢 Bullish"
        elif self.market_sentiment_score < -0.3:
            return "🔴 Bearish"
        else:
            return "🟡 Neutral"

@dataclass
class MarketData:
    """
    Container for comprehensive market data
    
    OOP Principles Applied:
    - Encapsulation: Internal data structure hidden
    - Composition: Contains stocks and metrics
    - Single Responsibility: Manages market data collection
    """
    
    # Core data
    stocks: List[Stock]
    metrics: MarketMetrics
    
    # Metadata
    market_type: MarketType
    data_source: str
    last_updated: datetime
    
    # Additional information
    market_status: Optional[str] = None
    notes: Optional[str] = None
    
    def __post_init__(self):
        """Validate and initialize data"""
        if not self.stocks:
            self.stocks = []
        
        # Ensure metrics match stock data
        if len(self.stocks) != self.metrics.total_stocks:
            self._recalculate_metrics()
    
    def _recalculate_metrics(self):
        """Recalculate metrics based on current stock data"""
        total = len(self.stocks)
        gaining = sum(1 for stock in self.stocks if stock.is_gaining)
        losing = sum(1 for stock in self.stocks if stock.is_losing)
        unchanged = total - gaining - losing
        
        # Calculate average change
        changes = [stock.change_percent for stock in self.stocks if stock.change_percent is not None]
        avg_change = sum(changes) / len(changes) if changes else None
        
        # Calculate total volume
        volumes = [stock.volume for stock in self.stocks if stock.volume is not None]
        total_volume = sum(volumes) if volumes else None
        
        # Update metrics
        self.metrics.total_stocks = total
        self.metrics.gaining_stocks = gaining
        self.metrics.losing_stocks = losing
        self.metrics.unchanged_stocks = unchanged
        self.metrics.average_change_percent = avg_change
        self.metrics.total_volume = total_volume
    
    def get_top_gainers(self, limit: int = 5) -> List[Stock]:
        """Get top performing stocks"""
        return sorted(
            [s for s in self.stocks if s.change_percent is not None],
            key=lambda x: x.change_percent,
            reverse=True
        )[:limit]
    
    def get_top_losers(self, limit: int = 5) -> List[Stock]:
        """Get worst performing stocks"""
        return sorted(
            [s for s in self.stocks if s.change_percent is not None],
            key=lambda x: x.change_percent
        )[:limit]
    
    def get_by_symbol(self, symbol: str) -> Optional[Stock]:
        """Find stock by symbol"""
        for stock in self.stocks:
            if stock.symbol.upper() == symbol.upper():
                return stock
        return None
    
    def filter_by_exchange(self, exchange: str) -> List[Stock]:
        """Filter stocks by exchange"""
        return [stock for stock in self.stocks if stock.exchange.upper() == exchange.upper()]
    
    def get_market_summary(self) -> Dict[str, Any]:
        """Get comprehensive market summary"""
        return {
            "total_stocks": self.metrics.total_stocks,
            "gaining_percentage": self.metrics.gaining_percentage,
            "losing_percentage": self.metrics.losing_percentage,
            "market_sentiment": self.metrics.market_sentiment_label,
            "average_change": self.metrics.average_change_percent,
            "total_volume": self.metrics.total_volume,
            "last_updated": self.last_updated.isoformat(),
            "market_status": self.market_status
        }
    
    def __len__(self) -> int:
        """Return number of stocks"""
        return len(self.stocks)
    
    def __iter__(self):
        """Make iterable over stocks"""
        return iter(self.stocks)
    
    def __str__(self) -> str:
        """String representation"""
        return f"MarketData({self.market_type.value}, {len(self.stocks)} stocks, {self.metrics.market_sentiment_label})"
