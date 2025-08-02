"""
Market Data Use Case
Handles business logic for retrieving market data
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class GetMarketDataUseCase:
    """Use case for getting market data"""
    
    def __init__(self, market_repository=None):
        self.market_repository = market_repository
    
    def execute(self, symbols: List[str] = None) -> Dict[str, Any]:
        """Execute market data retrieval"""
        return self._generate_sample_market_data()
    
    def _generate_sample_market_data(self) -> Dict[str, Any]:
        """Generate sample market data"""
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA', 'AMD', 'ORCL']
        companies = ['Apple Inc.', 'Microsoft Corp.', 'Alphabet Inc.', 'Amazon.com Inc.', 'Tesla Inc.',
                    'Meta Platforms Inc.', 'Netflix Inc.', 'NVIDIA Corp.', 'Advanced Micro Devices Inc.', 'Oracle Corp.']
        
        data = []
        for i, (symbol, company) in enumerate(zip(symbols, companies)):
            base_price = np.random.uniform(50, 400)
            change_pct = np.random.uniform(-5, 5)
            change_amount = base_price * (change_pct / 100)
            
            data.append({
                'Symbol': symbol,
                'Company': company,
                'Price': round(base_price, 2),
                'Change': round(change_amount, 2),
                'Change_Pct': round(change_pct, 2),
                'Volume': np.random.randint(1000000, 100000000),
                'Market_Cap': round(np.random.uniform(100, 3000), 1),  # in billions
                'PE_Ratio': round(np.random.uniform(15, 35), 1),
                'Day_High': round(base_price * 1.05, 2),
                'Day_Low': round(base_price * 0.95, 2),
                'Week_52_High': round(base_price * 1.3, 2),
                'Week_52_Low': round(base_price * 0.7, 2)
            })
        
        df = pd.DataFrame(data)
        
        return {
            'data': df,
            'summary': {
                'total_stocks': len(df),
                'gainers': len(df[df['Change_Pct'] > 0]),
                'losers': len(df[df['Change_Pct'] < 0]),
                'avg_change': df['Change_Pct'].mean(),
                'total_volume': df['Volume'].sum(),
                'top_performer': df.loc[df['Change_Pct'].idxmax(), 'Symbol'],
                'worst_performer': df.loc[df['Change_Pct'].idxmin(), 'Symbol']
            }
        }

# Create instance for export
get_market_data_use_case = GetMarketDataUseCase()
