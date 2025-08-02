"""
World Clock Component
Displays global financial market times and status
"""
import streamlit as st
from datetime import datetime
import pytz
from typing import Dict, Any

from ...domain.entities.market import Market, MarketStatus, MarketRegion
from datetime import time

class WorldClockComponent:
    """
    Component for displaying world financial market clocks
    
    Clean Code Principles:
    - Single Responsibility: Only handles world clock display
    - Separation of Concerns: UI logic separated from business logic
    - Reusable component design
    """
    
    def __init__(self):
        """Initialize with global market data"""
        self._markets = self._get_global_markets()
    
    def render(self, container=None):
        """
        Render the world clock component
        
        Args:
            container: Streamlit container to render in (default: sidebar)
        """
        if container is None:
            container = st.sidebar
        
        container.markdown("### 🌍 Global Financial Markets")
        container.markdown("---")
        
        # Group markets by region
        regions = self._group_markets_by_region()
        
        for region_name, markets in regions.items():
            with container.expander(f"{region_name} ({len(markets)} markets)"):
                for market in markets:
                    self._render_market_card(market, container)
    
    def _get_global_markets(self) -> list[Market]:
        """Get list of global financial markets"""
        return [
            # Americas
            Market("NYSE", "New York Stock Exchange", "US", "🇺🇸", "America/New_York", 
                   MarketRegion.AMERICAS, time(9, 30), time(16, 0), currency="USD"),
            Market("NASDAQ", "NASDAQ", "US", "🇺🇸", "America/New_York", 
                   MarketRegion.AMERICAS, time(9, 30), time(16, 0), currency="USD"),
            Market("TSX", "Toronto Stock Exchange", "CA", "🇨🇦", "America/Toronto", 
                   MarketRegion.AMERICAS, time(9, 30), time(16, 0), currency="CAD"),
            Market("BOVESPA", "B3 - Brasil Bolsa Balcão", "BR", "🇧🇷", "America/Sao_Paulo", 
                   MarketRegion.AMERICAS, time(10, 0), time(17, 0), currency="BRL"),
            
            # Europe
            Market("LSE", "London Stock Exchange", "GB", "🇬🇧", "Europe/London", 
                   MarketRegion.EUROPE, time(8, 0), time(16, 30), currency="GBP"),
            Market("DAX", "Frankfurt Stock Exchange", "DE", "🇩🇪", "Europe/Berlin", 
                   MarketRegion.EUROPE, time(9, 0), time(17, 30), currency="EUR"),
            Market("Euronext", "Euronext Paris", "FR", "🇫🇷", "Europe/Paris", 
                   MarketRegion.EUROPE, time(9, 0), time(17, 30), currency="EUR"),
            Market("BIST", "Borsa Istanbul", "TR", "🇹🇷", "Europe/Istanbul", 
                   MarketRegion.EUROPE, time(10, 0), time(18, 0), currency="TRY"),
            
            # Asia-Pacific
            Market("TSE", "Tokyo Stock Exchange", "JP", "🇯🇵", "Asia/Tokyo", 
                   MarketRegion.ASIA_PACIFIC, time(9, 0), time(15, 0), currency="JPY"),
            Market("SSE", "Shanghai Stock Exchange", "CN", "🇨🇳", "Asia/Shanghai", 
                   MarketRegion.ASIA_PACIFIC, time(9, 30), time(15, 0), currency="CNY"),
            Market("HKEX", "Hong Kong Stock Exchange", "HK", "🇭🇰", "Asia/Hong_Kong", 
                   MarketRegion.ASIA_PACIFIC, time(9, 30), time(16, 0), currency="HKD"),
            Market("ASX", "Australian Securities Exchange", "AU", "🇦🇺", "Australia/Sydney", 
                   MarketRegion.ASIA_PACIFIC, time(10, 0), time(16, 0), currency="AUD"),
            
            # MENA & Africa
            Market("DFM", "Dubai Financial Market", "AE", "🇦🇪", "Asia/Dubai", 
                   MarketRegion.MENA_AFRICA, time(10, 0), time(14, 0), currency="AED"),
            Market("Tadawul", "Saudi Stock Exchange", "SA", "🇸🇦", "Asia/Riyadh", 
                   MarketRegion.MENA_AFRICA, time(10, 0), time(15, 0), currency="SAR"),
        ]
    
    def _group_markets_by_region(self) -> Dict[str, list[Market]]:
        """Group markets by geographical region"""
        regions = {
            "🌎 Americas": [],
            "🌍 Europe": [],
            "🌏 Asia-Pacific": [],
            "🌍 MENA & Africa": []
        }
        
        region_map = {
            MarketRegion.AMERICAS: "🌎 Americas",
            MarketRegion.EUROPE: "🌍 Europe", 
            MarketRegion.ASIA_PACIFIC: "🌏 Asia-Pacific",
            MarketRegion.MENA_AFRICA: "🌍 MENA & Africa"
        }
        
        for market in self._markets:
            region_key = region_map.get(market.region, "🌍 Other")
            if region_key in regions:
                regions[region_key].append(market)
        
        return regions
    
    def _render_market_card(self, market: Market, container):
        """Render individual market card"""
        # Get current status and time
        current_time = market.get_formatted_time()
        current_date = market.get_formatted_date()
        status = market.current_status
        
        # Create market card HTML
        card_html = f"""
        <div style="padding: 8px; margin: 4px 0; border-left: 3px solid {market.status_color}; 
                    background-color: rgba(255,255,255,0.05); border-radius: 5px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="font-size: 0.9em;">{market.display_name}</strong><br>
                    <span style="font-size: 1.1em; font-weight: bold;">{current_time}</span>
                    <span style="font-size: 0.8em; color: #888;"> ({current_date})</span>
                </div>
                <div style="text-align: right;">
                    <span style="color: {market.status_color}; font-weight: bold; font-size: 0.8em;">
                        {market.status_emoji} {status.value.upper()}
                    </span><br>
                    <span style="font-size: 0.7em; color: #666;">
                        {market.get_trading_hours()}
                    </span>
                </div>
            </div>
        """
        
        # Add countdown information
        if status == MarketStatus.CLOSED:
            time_until_open = market.time_until_open()
            if time_until_open:
                card_html += f"""
                <div style="margin-top: 4px; font-size: 0.7em; color: #999;">
                    Opens in: {time_until_open}
                </div>
                """
        elif status == MarketStatus.OPEN:
            time_until_close = market.time_until_close()
            if time_until_close:
                card_html += f"""
                <div style="margin-top: 4px; font-size: 0.7em; color: #999;">
                    Closes in: {time_until_close}
                </div>
                """
        
        card_html += "</div>"
        
        container.markdown(card_html, unsafe_allow_html=True)
    
    def get_market_by_code(self, code: str) -> Market:
        """Get market by code"""
        for market in self._markets:
            if market.code.upper() == code.upper():
                return market
        return None
    
    def get_open_markets(self) -> list[Market]:
        """Get currently open markets"""
        return [market for market in self._markets if market.is_trading]
    
    def get_markets_summary(self) -> Dict[str, Any]:
        """Get summary of all markets"""
        open_count = len(self.get_open_markets())
        total_count = len(self._markets)
        
        return {
            "total_markets": total_count,
            "open_markets": open_count,
            "closed_markets": total_count - open_count,
            "open_percentage": (open_count / total_count * 100) if total_count > 0 else 0
        }
