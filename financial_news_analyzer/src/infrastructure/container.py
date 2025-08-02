"""
Dependency Injection Container
Manages application dependencies and services
"""
from typing import Dict, Any, Optional
import logging

from ..domain.services.sentiment_analysis_service import SentimentAnalysisService
from ..domain.services.news_analysis_service import NewsAnalysisService  
from ..domain.services.market_analysis_service import MarketAnalysisService
from ..application.use_cases.get_financial_news_use_case import GetFinancialNewsUseCase

class Container:
    """
    Simple dependency injection container
    
    Design Patterns:
    - Singleton Pattern: Single instance of container
    - Factory Pattern: Creates service instances
    - Service Locator Pattern: Centralized service access
    """
    
    _instance: Optional['Container'] = None
    _services: Dict[str, Any] = {}
    _initialized: bool = False
    
    def __new__(cls):
        """Ensure singleton instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize container if not already done"""
        if not self._initialized:
            self._initialize_services()
            self._initialized = True
    
    def _initialize_services(self):
        """Initialize all application services"""
        try:
            # Initialize core services
            self._services['sentiment_service'] = SentimentAnalysisService()
            self._services['news_analysis_service'] = NewsAnalysisService()
            self._services['market_analysis_service'] = MarketAnalysisService()
            
            # Initialize repositories (would be real implementations in production)
            from .repositories.in_memory_news_repository import InMemoryNewsRepository
            from .repositories.in_memory_market_repository import InMemoryMarketRepository
            
            self._services['news_repository'] = InMemoryNewsRepository()
            self._services['market_repository'] = InMemoryMarketRepository()
            
            # Initialize use cases
            self._services['get_news_use_case'] = GetFinancialNewsUseCase(
                self._services['news_repository']
            )
            
            logging.info("Container initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize container: {e}")
            raise
    
    def get_service(self, service_name: str) -> Any:
        """
        Get service by name
        
        Args:
            service_name: Name of the service to retrieve
            
        Returns:
            Service instance
            
        Raises:
            KeyError: If service not found
        """
        if service_name not in self._services:
            raise KeyError(f"Service '{service_name}' not found in container")
        
        return self._services[service_name]
    
    def register_service(self, service_name: str, service_instance: Any):
        """
        Register a service instance
        
        Args:
            service_name: Name to register service under
            service_instance: Service instance to register
        """
        self._services[service_name] = service_instance
        logging.info(f"Service '{service_name}' registered")
    
    def is_available(self, service_name: str) -> bool:
        """Check if service is available"""
        return service_name in self._services
    
    def get_all_services(self) -> Dict[str, Any]:
        """Get all registered services"""
        return self._services.copy()
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on all services"""
        health_status = {
            "container_status": "healthy",
            "services_count": len(self._services),
            "services": {}
        }
        
        for service_name, service in self._services.items():
            try:
                # Basic health check - just verify service exists and is not None
                if service is not None:
                    health_status["services"][service_name] = "healthy"
                else:
                    health_status["services"][service_name] = "unhealthy"
                    health_status["container_status"] = "degraded"
            except Exception as e:
                health_status["services"][service_name] = f"error: {str(e)}"
                health_status["container_status"] = "degraded"
        
        return health_status

# Global container instance
container = Container()
