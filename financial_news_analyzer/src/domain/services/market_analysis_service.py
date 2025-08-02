"""
Market Analysis Service
Comprehensive market data analysis and insights
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import statistics

from ..entities.market_data import MarketData, Stock, MarketMetrics, MarketType
from ..entities.analysis_result import AnalysisResult, AnalysisType, SentimentScore, SentimentType
from ..entities.market import Market, MarketStatus

class IMarketAnalyzer(ABC):
    """
    Interface for market analysis implementations
    
    SOLID Principles:
    - Interface Segregation: Clean, focused interface
    - Dependency Inversion: Depend on abstractions
    """
    
    @abstractmethod
    def analyze_market_trends(self, market_data: MarketData) -> Dict[str, Any]:
        """Analyze overall market trends"""
        pass
    
    @abstractmethod
    def identify_opportunities(self, stocks: List[Stock]) -> List[Dict[str, Any]]:
        """Identify trading opportunities"""
        pass
    
    @abstractmethod
    def calculate_risk_metrics(self, market_data: MarketData) -> Dict[str, float]:
        """Calculate risk metrics for the market"""
        pass

class TechnicalMarketAnalyzer(IMarketAnalyzer):
    """
    Technical analysis focused market analyzer
    
    Clean Code Principles:
    - Single Responsibility: Handles technical market analysis only
    - DRY: Reusable calculation methods
    - Meaningful names for clarity
    """
    
    def __init__(self):
        """Initialize with technical analysis parameters"""
        self._volatility_threshold = 0.05  # 5% threshold for high volatility
        self._momentum_threshold = 0.03   # 3% threshold for strong momentum
        self._volume_multiplier = 1.5     # 1.5x average volume for unusual activity
    
    def analyze_market_trends(self, market_data: MarketData) -> Dict[str, Any]:
        """
        Analyze overall market trends using technical indicators
        
        Args:
            market_data: Market data to analyze
            
        Returns:
            Dictionary with trend analysis results
        """
        if not market_data.stocks:
            return {"trend": "unknown", "strength": 0.0, "confidence": 0.0}
        
        # Calculate trend metrics
        gaining_ratio = market_data.metrics.gaining_percentage / 100
        losing_ratio = market_data.metrics.losing_percentage / 100
        
        # Calculate average change
        changes = [s.change_percent for s in market_data.stocks if s.change_percent is not None]
        avg_change = statistics.mean(changes) if changes else 0.0
        
        # Calculate trend strength
        trend_strength = abs(avg_change) / 100  # Normalize to 0-1 scale
        
        # Determine trend direction
        if gaining_ratio > 0.6 and avg_change > 1.0:
            trend = "strong_bullish"
        elif gaining_ratio > 0.55 and avg_change > 0.5:
            trend = "bullish"
        elif losing_ratio > 0.6 and avg_change < -1.0:
            trend = "strong_bearish"
        elif losing_ratio > 0.55 and avg_change < -0.5:
            trend = "bearish"
        else:
            trend = "neutral"
        
        # Calculate confidence based on data quality
        confidence = self._calculate_trend_confidence(market_data)
        
        # Identify supporting factors
        supporting_factors = self._identify_trend_factors(market_data, trend)
        
        return {
            "trend": trend,
            "direction": "up" if avg_change > 0 else "down" if avg_change < 0 else "sideways",
            "strength": min(trend_strength, 1.0),
            "confidence": confidence,
            "average_change": avg_change,
            "gaining_ratio": gaining_ratio,
            "losing_ratio": losing_ratio,
            "supporting_factors": supporting_factors,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def identify_opportunities(self, stocks: List[Stock]) -> List[Dict[str, Any]]:
        """
        Identify potential trading opportunities
        
        Args:
            stocks: List of stocks to analyze
            
        Returns:
            List of opportunity dictionaries
        """
        opportunities = []
        
        for stock in stocks:
            if not stock.change_percent or not stock.volume:
                continue
            
            opportunity = self._analyze_stock_opportunity(stock)
            if opportunity:
                opportunities.append(opportunity)
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        return opportunities[:20]  # Return top 20 opportunities
    
    def calculate_risk_metrics(self, market_data: MarketData) -> Dict[str, float]:
        """
        Calculate comprehensive risk metrics
        
        Args:
            market_data: Market data to analyze
            
        Returns:
            Dictionary with risk metrics
        """
        if not market_data.stocks:
            return {"overall_risk": 0.5, "volatility_risk": 0.5, "concentration_risk": 0.5}
        
        # Calculate volatility risk
        changes = [abs(s.change_percent) for s in market_data.stocks if s.change_percent is not None]
        volatility = statistics.stdev(changes) if len(changes) > 1 else 0.0
        volatility_risk = min(volatility / 10.0, 1.0)  # Normalize to 0-1
        
        # Calculate concentration risk (how much market depends on few stocks)
        total_market_cap = sum(s.market_cap for s in market_data.stocks if s.market_cap)
        if total_market_cap > 0:
            # Calculate Herfindahl index
            market_caps = [s.market_cap for s in market_data.stocks if s.market_cap]
            hhi = sum((cap / total_market_cap) ** 2 for cap in market_caps)
            concentration_risk = min(hhi * 2, 1.0)  # Normalize
        else:
            concentration_risk = 0.5
        
        # Calculate liquidity risk
        volumes = [s.volume for s in market_data.stocks if s.volume]
        avg_volume = statistics.mean(volumes) if volumes else 0
        low_volume_count = sum(1 for v in volumes if v < avg_volume * 0.5)
        liquidity_risk = (low_volume_count / len(volumes)) if volumes else 0.5
        
        # Calculate overall risk
        overall_risk = (volatility_risk * 0.4 + concentration_risk * 0.3 + liquidity_risk * 0.3)
        
        return {
            "overall_risk": overall_risk,
            "volatility_risk": volatility_risk,
            "concentration_risk": concentration_risk,
            "liquidity_risk": liquidity_risk,
            "volatility_pct": volatility,
            "herfindahl_index": concentration_risk / 2 if total_market_cap > 0 else 0
        }
    
    def _calculate_trend_confidence(self, market_data: MarketData) -> float:
        """Calculate confidence in trend analysis"""
        confidence = 0.5  # Base confidence
        
        # Boost confidence with more data points
        stock_count = len(market_data.stocks)
        if stock_count > 100:
            confidence += 0.2
        elif stock_count > 50:
            confidence += 0.1
        
        # Boost confidence with volume data
        with_volume = sum(1 for s in market_data.stocks if s.volume)
        volume_ratio = with_volume / stock_count if stock_count > 0 else 0
        confidence += volume_ratio * 0.2
        
        # Boost confidence with consistent direction
        changes = [s.change_percent for s in market_data.stocks if s.change_percent is not None]
        if changes:
            positive_changes = sum(1 for c in changes if c > 0)
            negative_changes = sum(1 for c in changes if c < 0)
            consistency = abs(positive_changes - negative_changes) / len(changes)
            confidence += consistency * 0.1
        
        return min(confidence, 1.0)
    
    def _identify_trend_factors(self, market_data: MarketData, trend: str) -> List[str]:
        """Identify factors supporting the current trend"""
        factors = []
        
        # Volume factors
        volumes = [s.volume for s in market_data.stocks if s.volume]
        if volumes:
            avg_volume = statistics.mean(volumes)
            high_volume_count = sum(1 for v in volumes if v > avg_volume * self._volume_multiplier)
            if high_volume_count > len(volumes) * 0.3:
                factors.append("High trading volume supporting trend")
        
        # Sector breadth
        gaining_pct = market_data.metrics.gaining_percentage
        losing_pct = market_data.metrics.losing_percentage
        
        if gaining_pct > 70:
            factors.append("Broad-based market participation")
        elif losing_pct > 70:
            factors.append("Widespread selling pressure")
        
        # Momentum factors
        changes = [s.change_percent for s in market_data.stocks if s.change_percent is not None]
        if changes:
            strong_moves = sum(1 for c in changes if abs(c) > self._momentum_threshold * 100)
            if strong_moves > len(changes) * 0.2:
                factors.append("Strong price momentum across market")
        
        return factors
    
    def _analyze_stock_opportunity(self, stock: Stock) -> Optional[Dict[str, Any]]:
        """Analyze individual stock for opportunities"""
        if not stock.change_percent or not stock.volume:
            return None
        
        opportunity_score = 0.0
        signals = []
        opportunity_type = "unknown"
        
        # Momentum signals
        if stock.change_percent > 5.0:
            opportunity_score += 0.3
            signals.append("Strong upward momentum")
            opportunity_type = "momentum_long"
        elif stock.change_percent < -5.0:
            opportunity_score += 0.3
            signals.append("Strong downward momentum")
            opportunity_type = "momentum_short"
        
        # Volume signals
        if stock.average_volume and stock.volume > stock.average_volume * self._volume_multiplier:
            opportunity_score += 0.2
            signals.append("Unusual volume activity")
        
        # Volatility signals
        if abs(stock.change_percent) > 3.0:
            opportunity_score += 0.1
            signals.append("High volatility")
        
        # Gap signals (if we had previous close data)
        if stock.previous_close and stock.open_price:
            gap_percent = ((stock.open_price - stock.previous_close) / stock.previous_close) * 100
            if abs(gap_percent) > 2.0:
                opportunity_score += 0.15
                signals.append(f"Significant gap {'up' if gap_percent > 0 else 'down'}")
        
        # Only return opportunities with meaningful scores
        if opportunity_score < 0.3:
            return None
        
        return {
            "symbol": stock.symbol,
            "name": stock.name,
            "score": opportunity_score,
            "type": opportunity_type,
            "current_price": float(stock.current_price),
            "change_percent": stock.change_percent,
            "volume": stock.volume,
            "signals": signals,
            "risk_level": self._assess_stock_risk(stock)
        }
    
    def _assess_stock_risk(self, stock: Stock) -> str:
        """Assess risk level for individual stock"""
        if not stock.change_percent:
            return "medium"
        
        volatility = abs(stock.change_percent)
        
        if volatility > 8.0:
            return "high"
        elif volatility > 3.0:
            return "medium"
        else:
            return "low"

class MarketAnalysisService:
    """
    Service for comprehensive market analysis
    
    Design Patterns:
    - Strategy Pattern: Different analysis strategies
    - Factory Pattern: Create appropriate analyzers
    - Observer Pattern: Notify about analysis updates
    """
    
    def __init__(self, analyzer: Optional[IMarketAnalyzer] = None):
        """Initialize service with analyzer"""
        self._analyzer = analyzer or TechnicalMarketAnalyzer()
    
    def analyze_market_comprehensive(self, market_data: MarketData) -> AnalysisResult:
        """
        Perform comprehensive market analysis
        
        Args:
            market_data: Market data to analyze
            
        Returns:
            Complete analysis result
        """
        # Perform trend analysis
        trend_analysis = self._analyzer.analyze_market_trends(market_data)
        
        # Identify opportunities
        opportunities = self._analyzer.identify_opportunities(market_data.stocks)
        
        # Calculate risk metrics
        risk_metrics = self._analyzer.calculate_risk_metrics(market_data)
        
        # Generate market sentiment
        market_sentiment = self._generate_market_sentiment(market_data, trend_analysis)
        
        # Generate insights
        insights = self._generate_market_insights(market_data, trend_analysis, risk_metrics)
        
        # Generate recommendations
        recommendations = self._generate_market_recommendations(trend_analysis, risk_metrics, opportunities)
        
        # Calculate overall confidence
        confidence = self._calculate_analysis_confidence(market_data, trend_analysis)
        
        # Create analysis result
        analysis_result = AnalysisResult(
            id=f"market_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            analysis_type=AnalysisType.TECHNICAL_ANALYSIS,
            subject_id=f"market_{market_data.market_type.value}",
            sentiment_score=market_sentiment,
            impact_score=self._calculate_market_impact(trend_analysis, risk_metrics),
            confidence_level=confidence,
            summary=self._generate_market_summary(market_data, trend_analysis),
            key_insights=insights,
            recommendations=recommendations,
            risk_level=self._determine_market_risk_level(risk_metrics),
            analysis_method="Technical Market Analysis",
            data_sources=[market_data.data_source],
            created_at=datetime.now(),
            analyst="AI_Market_Analyzer",
            metadata={
                "market_type": market_data.market_type.value,
                "stocks_analyzed": len(market_data.stocks),
                "trend_direction": trend_analysis.get("direction", "unknown"),
                "trend_strength": trend_analysis.get("strength", 0.0),
                "opportunities_found": len(opportunities),
                "overall_risk": risk_metrics.get("overall_risk", 0.5)
            }
        )
        
        return analysis_result
    
    def analyze_stock_performance(self, stocks: List[Stock]) -> Dict[str, Any]:
        """Analyze performance metrics for stocks"""
        if not stocks:
            return {"top_gainers": [], "top_losers": [], "most_active": []}
        
        # Sort by performance
        gainers = sorted(
            [s for s in stocks if s.change_percent and s.change_percent > 0],
            key=lambda x: x.change_percent,
            reverse=True
        )[:10]
        
        losers = sorted(
            [s for s in stocks if s.change_percent and s.change_percent < 0],
            key=lambda x: x.change_percent
        )[:10]
        
        # Sort by volume
        active = sorted(
            [s for s in stocks if s.volume],
            key=lambda x: x.volume,
            reverse=True
        )[:10]
        
        return {
            "top_gainers": [self._stock_to_dict(s) for s in gainers],
            "top_losers": [self._stock_to_dict(s) for s in losers],
            "most_active": [self._stock_to_dict(s) for s in active],
            "analysis_time": datetime.now().isoformat()
        }
    
    def compare_markets(self, markets_data: List[MarketData]) -> Dict[str, Any]:
        """Compare performance across different markets"""
        if not markets_data:
            return {"comparison": [], "best_performer": None, "worst_performer": None}
        
        comparisons = []
        
        for market_data in markets_data:
            if not market_data.stocks:
                continue
            
            avg_change = market_data.metrics.average_change_percent or 0.0
            
            comparison = {
                "market_type": market_data.market_type.value,
                "average_change": avg_change,
                "gaining_percentage": market_data.metrics.gaining_percentage,
                "total_stocks": market_data.metrics.total_stocks,
                "sentiment": market_data.metrics.market_sentiment_label,
                "last_updated": market_data.last_updated.isoformat()
            }
            comparisons.append(comparison)
        
        # Find best and worst performers
        if comparisons:
            best = max(comparisons, key=lambda x: x["average_change"])
            worst = min(comparisons, key=lambda x: x["average_change"])
        else:
            best = worst = None
        
        return {
            "comparison": comparisons,
            "best_performer": best,
            "worst_performer": worst,
            "comparison_time": datetime.now().isoformat()
        }
    
    def _generate_market_sentiment(self, market_data: MarketData, 
                                 trend_analysis: Dict[str, Any]) -> SentimentScore:
        """Generate overall market sentiment score"""
        gaining_ratio = market_data.metrics.gaining_percentage / 100
        avg_change = trend_analysis.get("average_change", 0.0)
        
        # Calculate sentiment score based on market metrics
        sentiment_score = (gaining_ratio - 0.5) * 2  # Convert to -1 to 1 scale
        sentiment_score += (avg_change / 100)  # Add momentum component
        sentiment_score = max(-1.0, min(1.0, sentiment_score))  # Clamp to range
        
        # Calculate confidence
        confidence = trend_analysis.get("confidence", 0.5)
        
        # Determine sentiment type
        if sentiment_score > 0.6:
            sentiment_type = SentimentType.VERY_POSITIVE
        elif sentiment_score > 0.2:
            sentiment_type = SentimentType.POSITIVE
        elif sentiment_score > -0.2:
            sentiment_type = SentimentType.NEUTRAL
        elif sentiment_score > -0.6:
            sentiment_type = SentimentType.NEGATIVE
        else:
            sentiment_type = SentimentType.VERY_NEGATIVE
        
        return SentimentScore(
            score=sentiment_score,
            confidence=confidence,
            sentiment_type=sentiment_type,
            positive_probability=max(0, sentiment_score),
            negative_probability=max(0, -sentiment_score),
            neutral_probability=1 - abs(sentiment_score),
            analyzed_text_length=None,
            key_phrases=trend_analysis.get("supporting_factors", [])
        )
    
    def _generate_market_insights(self, market_data: MarketData, 
                                trend_analysis: Dict[str, Any], 
                                risk_metrics: Dict[str, float]) -> List[str]:
        """Generate market insights"""
        insights = []
        
        # Trend insights
        trend = trend_analysis.get("trend", "unknown")
        strength = trend_analysis.get("strength", 0.0)
        
        insights.append(f"Market trend: {trend.replace('_', ' ').title()} (strength: {strength:.1%})")
        
        # Performance insights
        gaining_pct = market_data.metrics.gaining_percentage
        insights.append(f"Market breadth: {gaining_pct:.1f}% of stocks advancing")
        
        # Risk insights
        overall_risk = risk_metrics.get("overall_risk", 0.5)
        risk_level = "High" if overall_risk > 0.7 else "Medium" if overall_risk > 0.4 else "Low"
        insights.append(f"Risk assessment: {risk_level} risk environment")
        
        # Volume insights
        volumes = [s.volume for s in market_data.stocks if s.volume]
        if volumes:
            avg_volume = statistics.mean(volumes)
            insights.append(f"Average trading volume: {avg_volume:,.0f} shares")
        
        # Supporting factors
        factors = trend_analysis.get("supporting_factors", [])
        if factors:
            insights.extend(factors)
        
        return insights
    
    def _generate_market_recommendations(self, trend_analysis: Dict[str, Any], 
                                       risk_metrics: Dict[str, float], 
                                       opportunities: List[Dict[str, Any]]) -> List[str]:
        """Generate market recommendations"""
        recommendations = []
        
        trend = trend_analysis.get("trend", "unknown")
        overall_risk = risk_metrics.get("overall_risk", 0.5)
        
        # Trend-based recommendations
        if "bullish" in trend:
            recommendations.append("📈 Consider increasing equity exposure")
            recommendations.append("🎯 Look for momentum opportunities")
        elif "bearish" in trend:
            recommendations.append("📉 Consider defensive positioning")
            recommendations.append("🛡️ Implement risk management strategies")
        else:
            recommendations.append("⚖️ Maintain balanced portfolio allocation")
            recommendations.append("👀 Wait for clearer trend signals")
        
        # Risk-based recommendations
        if overall_risk > 0.7:
            recommendations.append("⚠️ High risk environment - reduce position sizes")
            recommendations.append("🔒 Implement strict stop-loss levels")
        elif overall_risk < 0.3:
            recommendations.append("✅ Low risk environment - consider increasing exposure")
        
        # Opportunity-based recommendations
        if opportunities:
            high_score_ops = [op for op in opportunities if op.get("score", 0) > 0.7]
            if high_score_ops:
                symbols = [op["symbol"] for op in high_score_ops[:3]]
                recommendations.append(f"🎯 High-potential opportunities: {', '.join(symbols)}")
        
        return recommendations
    
    def _calculate_analysis_confidence(self, market_data: MarketData, 
                                     trend_analysis: Dict[str, Any]) -> float:
        """Calculate overall analysis confidence"""
        base_confidence = 0.5
        
        # Data quality factors
        stock_count = len(market_data.stocks)
        if stock_count > 100:
            base_confidence += 0.2
        elif stock_count > 50:
            base_confidence += 0.1
        
        # Trend confidence
        trend_confidence = trend_analysis.get("confidence", 0.5)
        base_confidence += trend_confidence * 0.3
        
        return min(base_confidence, 1.0)
    
    def _calculate_market_impact(self, trend_analysis: Dict[str, Any], 
                               risk_metrics: Dict[str, float]) -> float:
        """Calculate potential market impact score"""
        trend_strength = trend_analysis.get("strength", 0.0)
        overall_risk = risk_metrics.get("overall_risk", 0.5)
        
        # Impact is higher with stronger trends and higher risk
        impact = (trend_strength + overall_risk) / 2
        
        return min(impact, 1.0)
    
    def _determine_market_risk_level(self, risk_metrics: Dict[str, float]) -> str:
        """Determine overall market risk level"""
        overall_risk = risk_metrics.get("overall_risk", 0.5)
        
        if overall_risk > 0.7:
            return "high"
        elif overall_risk > 0.4:
            return "medium"
        else:
            return "low"
    
    def _generate_market_summary(self, market_data: MarketData, 
                               trend_analysis: Dict[str, Any]) -> str:
        """Generate market analysis summary"""
        trend = trend_analysis.get("trend", "unknown")
        gaining_pct = market_data.metrics.gaining_percentage
        stock_count = len(market_data.stocks)
        
        return (f"Technical analysis of {stock_count} stocks shows {trend.replace('_', ' ')} "
                f"trend with {gaining_pct:.1f}% of stocks advancing. "
                f"Analysis based on {market_data.market_type.value} market data.")
    
    def _stock_to_dict(self, stock: Stock) -> Dict[str, Any]:
        """Convert stock to dictionary for serialization"""
        return {
            "symbol": stock.symbol,
            "name": stock.name,
            "current_price": float(stock.current_price),
            "change_percent": stock.change_percent,
            "change_amount": float(stock.change_amount) if stock.change_amount else None,
            "volume": stock.volume,
            "market_cap": float(stock.market_cap) if stock.market_cap else None
        }
