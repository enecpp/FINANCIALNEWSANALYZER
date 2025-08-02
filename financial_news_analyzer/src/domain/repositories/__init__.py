"""
Domain Repositories Package
Abstract interfaces for data access
"""
from .news_repository import INewsRepository
from .market_data_repository import IMarketDataRepository

__all__ = [
    'INewsRepository',
    'IMarketDataRepository'
]
