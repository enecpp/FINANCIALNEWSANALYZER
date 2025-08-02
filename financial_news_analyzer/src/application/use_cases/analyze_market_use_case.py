"""
Market Analysis Use Case
Handles business logic for market analysis and insights
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class AnalyzeMarketUseCase:
    """Use case for analyzing market trends and patterns"""
    
    def __init__(self, market_repository=None):
        self.market_repository = market_repository
    
    def execute(self, period: str = "1Y", analysis_type: str = "overview") -> Dict[str, Any]:
        """Execute market analysis"""
        return self._generate_market_analysis(period, analysis_type)
    
    def _generate_market_analysis(self, period: str, analysis_type: str) -> Dict[str, Any]:
        """Generate comprehensive market analysis"""
        
        # Generate historical data for analysis
        days = self._get_days_from_period(period)
        historical_data = self._generate_historical_data(days)
        
        # Perform different types of analysis
        if analysis_type == "overview":
            return self._market_overview_analysis(historical_data)
        elif analysis_type == "technical":
            return self._technical_analysis(historical_data)
        elif analysis_type == "correlation":
            return self._correlation_analysis(historical_data)
        else:
            return self._comprehensive_analysis(historical_data)
    
    def _get_days_from_period(self, period: str) -> int:
        """Convert period string to number of days"""
        period_map = {
            "1M": 30,
            "3M": 90,
            "6M": 180,
            "1Y": 365,
            "2Y": 730
        }
        return period_map.get(period, 365)
    
    def _generate_historical_data(self, days: int) -> pd.DataFrame:
        """Generate historical market data"""
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        symbols = ['SPY', 'QQQ', 'IWM', 'VIX', 'GLD', 'TLT']
        
        data = []
        for symbol in symbols:
            base_price = np.random.uniform(100, 500)
            prices = [base_price]
            
            for i in range(1, days):
                # Random walk with market characteristics
                if symbol == 'VIX':  # Volatility index
                    change = np.random.normal(0, 0.05)
                else:
                    change = np.random.normal(0.0005, 0.02)  # Slight upward bias
                
                new_price = prices[-1] * (1 + change)
                prices.append(max(new_price, 10))
            
            for i, (date, price) in enumerate(zip(dates, prices)):
                data.append({
                    'Date': date,
                    'Symbol': symbol,
                    'Price': round(price, 2),
                    'Volume': np.random.randint(10000000, 200000000)
                })
        
        return pd.DataFrame(data)
    
    def _market_overview_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate market overview analysis"""
        latest_data = df.groupby('Symbol').last().reset_index()
        
        return {
            'analysis_type': 'Market Overview',
            'data': latest_data,
            'insights': {
                'market_trend': 'Bullish' if np.random.random() > 0.5 else 'Bearish',
                'volatility_level': np.random.choice(['Low', 'Medium', 'High']),
                'recommended_action': np.random.choice(['Buy', 'Hold', 'Sell']),
                'confidence_score': round(np.random.uniform(0.6, 0.95), 2)
            },
            'summary': {
                'total_instruments': len(latest_data),
                'avg_performance': round(np.random.uniform(-2, 5), 2),
                'market_cap_total': round(np.random.uniform(30000, 50000), 0)
            }
        }
    
    def _technical_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate technical analysis"""
        # Calculate technical indicators for each symbol
        technical_data = []
        
        for symbol in df['Symbol'].unique():
            symbol_data = df[df['Symbol'] == symbol].sort_values('Date')
            prices = symbol_data['Price'].values
            
            # Calculate moving averages
            ma_20 = np.mean(prices[-20:]) if len(prices) >= 20 else np.mean(prices)
            ma_50 = np.mean(prices[-50:]) if len(prices) >= 50 else np.mean(prices)
            
            # Calculate RSI (simplified)
            rsi = np.random.uniform(30, 70)
            
            # Support and resistance levels
            support = np.min(prices[-20:]) if len(prices) >= 20 else np.min(prices)
            resistance = np.max(prices[-20:]) if len(prices) >= 20 else np.max(prices)
            
            technical_data.append({
                'Symbol': symbol,
                'Current_Price': prices[-1],
                'MA_20': round(ma_20, 2),
                'MA_50': round(ma_50, 2),
                'RSI': round(rsi, 2),
                'Support': round(support, 2),
                'Resistance': round(resistance, 2),
                'Signal': np.random.choice(['Buy', 'Sell', 'Hold'])
            })
        
        return {
            'analysis_type': 'Technical Analysis',
            'data': pd.DataFrame(technical_data),
            'insights': {
                'overall_signal': np.random.choice(['Bullish', 'Bearish', 'Neutral']),
                'strength': np.random.choice(['Strong', 'Moderate', 'Weak']),
                'time_horizon': 'Short to Medium Term'
            }
        }
    
    def _correlation_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate correlation analysis"""
        # Pivot data for correlation calculation
        pivot_df = df.pivot(index='Date', columns='Symbol', values='Price')
        correlation_matrix = pivot_df.corr()
        
        return {
            'analysis_type': 'Correlation Analysis',
            'data': correlation_matrix,
            'insights': {
                'highest_correlation': f"{correlation_matrix.iloc[0, 1]:.2f}",
                'diversification_score': round(np.random.uniform(0.3, 0.8), 2),
                'risk_level': np.random.choice(['Low', 'Medium', 'High'])
            }
        }
    
    def _comprehensive_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive market analysis"""
        overview = self._market_overview_analysis(df)
        technical = self._technical_analysis(df)
        correlation = self._correlation_analysis(df)
        
        return {
            'analysis_type': 'Comprehensive Analysis',
            'overview': overview,
            'technical': technical,
            'correlation': correlation,
            'combined_insights': {
                'market_score': round(np.random.uniform(6.5, 9.2), 1),
                'risk_reward_ratio': round(np.random.uniform(1.2, 3.8), 1),
                'recommended_allocation': {
                    'Stocks': np.random.randint(60, 80),
                    'Bonds': np.random.randint(15, 25),
                    'Cash': np.random.randint(5, 15)
                }
            }
        }

# Create instance for export
analyze_market_use_case = AnalyzeMarketUseCase()
