"""
Mock Market Service
Provides sample market data for development and testing
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random
import math

class MockMarketService:
    """Mock service for market data"""
    
    def __init__(self):
        self.symbols = {
            'AAPL': {'name': 'Apple Inc.', 'sector': 'Technology', 'base_price': 180},
            'MSFT': {'name': 'Microsoft Corp.', 'sector': 'Technology', 'base_price': 350},
            'GOOGL': {'name': 'Alphabet Inc.', 'sector': 'Technology', 'base_price': 140},
            'AMZN': {'name': 'Amazon.com Inc.', 'sector': 'Consumer Discretionary', 'base_price': 130},
            'TSLA': {'name': 'Tesla Inc.', 'sector': 'Automotive', 'base_price': 220},
            'META': {'name': 'Meta Platforms Inc.', 'sector': 'Technology', 'base_price': 320},
            'NFLX': {'name': 'Netflix Inc.', 'sector': 'Entertainment', 'base_price': 450},
            'NVDA': {'name': 'NVIDIA Corp.', 'sector': 'Technology', 'base_price': 900},
            'AMD': {'name': 'Advanced Micro Devices Inc.', 'sector': 'Technology', 'base_price': 140},
            'ORCL': {'name': 'Oracle Corp.', 'sector': 'Technology', 'base_price': 110}
        }
    
    def get_current_prices(self, symbols: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Get current market prices for symbols"""
        if symbols is None:
            symbols = list(self.symbols.keys())
        
        market_data = []
        
        for symbol in symbols:
            if symbol not in self.symbols:
                continue
                
            info = self.symbols[symbol]
            base_price = info['base_price']
            
            # Generate realistic price movement
            daily_change_pct = random.uniform(-5.0, 5.0)
            current_price = base_price * (1 + daily_change_pct / 100)
            change_amount = current_price - base_price
            
            # Generate volume
            avg_volume = random.randint(10000000, 100000000)
            volume = int(avg_volume * random.uniform(0.5, 2.0))
            
            # Calculate other metrics
            day_high = current_price * random.uniform(1.01, 1.05)
            day_low = current_price * random.uniform(0.95, 0.99)
            
            market_data.append({
                'symbol': symbol,
                'company_name': info['name'],
                'sector': info['sector'],
                'current_price': round(current_price, 2),
                'change_amount': round(change_amount, 2),
                'change_percent': round(daily_change_pct, 2),
                'volume': volume,
                'day_high': round(day_high, 2),
                'day_low': round(day_low, 2),
                'market_cap': round(random.uniform(500, 3000), 1),  # in billions
                'pe_ratio': round(random.uniform(15, 35), 1),
                'week_52_high': round(current_price * random.uniform(1.2, 1.5), 2),
                'week_52_low': round(current_price * random.uniform(0.6, 0.8), 2),
                'last_updated': datetime.now().isoformat()
            })
        
        return market_data
    
    def get_historical_data(self, symbol: str, period: str = "1Y") -> List[Dict[str, Any]]:
        """Get historical price data for a symbol"""
        if symbol not in self.symbols:
            return []
        
        # Determine number of days based on period
        period_days = {
            "1D": 1, "5D": 5, "1M": 30, "3M": 90, 
            "6M": 180, "1Y": 365, "2Y": 730, "5Y": 1825
        }
        days = period_days.get(period, 365)
        
        # Generate historical data
        dates = []
        current_date = datetime.now()
        for i in range(days):
            dates.append(current_date - timedelta(days=i))
        dates.reverse()
        
        base_price = self.symbols[symbol]['base_price']
        historical_data = []
        
        # Generate price series with realistic movement
        price = base_price
        for date in dates:
            # Random walk with slight upward bias
            daily_return = random.gauss(0.0005, 0.02)  # 0.05% average daily return, 2% volatility
            price = max(price * (1 + daily_return), 10)  # Ensure price doesn't go below $10
            
            # Generate OHLC data
            daily_volatility = random.uniform(0.005, 0.03)
            high = price * (1 + daily_volatility)
            low = price * (1 - daily_volatility)
            open_price = random.uniform(low, high)
            close_price = price
            
            volume = random.randint(5000000, 80000000)
            
            historical_data.append({
                'symbol': symbol,
                'date': date.strftime('%Y-%m-%d'),
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(close_price, 2),
                'volume': volume,
                'adjusted_close': round(close_price, 2)
            })
        
        return historical_data
    
    def get_market_indices(self) -> List[Dict[str, Any]]:
        """Get major market indices data"""
        indices = {
            '^GSPC': {'name': 'S&P 500', 'base_value': 4500},
            '^DJI': {'name': 'Dow Jones Industrial Average', 'base_value': 35000},
            '^IXIC': {'name': 'NASDAQ Composite', 'base_value': 14000},
            '^RUT': {'name': 'Russell 2000', 'base_value': 2000},
            '^VIX': {'name': 'CBOE Volatility Index', 'base_value': 20}
        }
        
        market_indices = []
        for symbol, info in indices.items():
            change_pct = random.uniform(-2.0, 2.0)
            if symbol == '^VIX':  # VIX behaves differently
                change_pct = random.uniform(-10.0, 10.0)
            
            current_value = info['base_value'] * (1 + change_pct / 100)
            change_amount = current_value - info['base_value']
            
            market_indices.append({
                'symbol': symbol,
                'name': info['name'],
                'current_value': round(current_value, 2),
                'change_amount': round(change_amount, 2),
                'change_percent': round(change_pct, 2),
                'last_updated': datetime.now().isoformat()
            })
        
        return market_indices
    
    def get_sector_performance(self) -> List[Dict[str, Any]]:
        """Get sector performance data"""
        sectors = [
            'Technology', 'Healthcare', 'Financial Services', 'Consumer Discretionary',
            'Communication Services', 'Industrials', 'Consumer Staples', 
            'Energy', 'Utilities', 'Real Estate', 'Materials'
        ]
        
        sector_data = []
        for sector in sectors:
            change_pct = random.uniform(-3.0, 3.0)
            
            sector_data.append({
                'sector': sector,
                'change_percent': round(change_pct, 2),
                'market_cap': round(random.uniform(1000, 15000), 1),  # in billions
                'pe_ratio': round(random.uniform(15, 30), 1),
                'dividend_yield': round(random.uniform(0.5, 4.0), 2)
            })
        
        return sorted(sector_data, key=lambda x: x['change_percent'], reverse=True)
    
    def get_market_summary(self) -> Dict[str, Any]:
        """Get overall market summary"""
        indices = self.get_market_indices()
        sectors = self.get_sector_performance()
        
        # Calculate market statistics
        sp500_change = next((idx['change_percent'] for idx in indices if idx['symbol'] == '^GSPC'), 0)
        vix_value = next((idx['current_value'] for idx in indices if idx['symbol'] == '^VIX'), 20)
        
        advancing_sectors = len([s for s in sectors if s['change_percent'] > 0])
        declining_sectors = len([s for s in sectors if s['change_percent'] < 0])
        
        return {
            'market_sentiment': 'Bullish' if sp500_change > 0 else 'Bearish',
            'volatility_level': 'High' if vix_value > 25 else 'Medium' if vix_value > 15 else 'Low',
            'advancing_sectors': advancing_sectors,
            'declining_sectors': declining_sectors,
            'total_market_cap': round(random.uniform(45000, 55000), 0),  # in billions
            'trading_volume': random.randint(3000000000, 6000000000),  # shares
            'last_updated': datetime.now().isoformat()
        }

# Create instance for export
mock_market_service = MockMarketService()
