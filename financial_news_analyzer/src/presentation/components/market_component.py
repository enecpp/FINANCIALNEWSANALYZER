"""
Market Component
Streamlit components for displaying market data
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List
import pandas as pd

class MarketComponent:
    """Component for rendering market-related UI elements"""
    
    @staticmethod
    def render_stock_card(stock_data: Dict[str, Any]) -> None:
        """Render a single stock card"""
        change_color = '#00D4AA' if stock_data.get('change_percent', 0) >= 0 else '#FF6B6B'
        change_symbol = '+' if stock_data.get('change_percent', 0) >= 0 else ''
        
        with st.container():
            st.markdown(f"""
            <div style="
                background: var(--secondary-bg);
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid {change_color};
                margin: 10px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="color: white; margin: 0;">{stock_data.get('symbol', 'N/A')}</h3>
                        <p style="color: #CCCCCC; margin: 5px 0;">
                            {stock_data.get('company_name', 'Company Name')}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <h3 style="color: white; margin: 0;">
                            ${stock_data.get('current_price', 0):.2f}
                        </h3>
                        <p style="color: {change_color}; margin: 5px 0; font-weight: bold;">
                            {change_symbol}{stock_data.get('change_amount', 0):.2f} 
                            ({change_symbol}{stock_data.get('change_percent', 0):.2f}%)
                        </p>
                    </div>
                </div>
                <div style="margin-top: 10px; font-size: 0.9em; color: #CCCCCC;">
                    Volume: {stock_data.get('volume', 0):,} | 
                    Market Cap: ${stock_data.get('market_cap', 0):.1f}B | 
                    P/E: {stock_data.get('pe_ratio', 0):.1f}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_candlestick_chart(historical_data: List[Dict[str, Any]], symbol: str) -> go.Figure:
        """Render candlestick chart for a stock"""
        df = pd.DataFrame(historical_data)
        
        if df.empty:
            return go.Figure()
        
        fig = go.Figure(data=go.Candlestick(
            x=pd.to_datetime(df['date']),
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            increasing_line_color='#00D4AA',
            decreasing_line_color='#FF6B6B',
            name=symbol
        ))
        
        fig.update_layout(
            title=f"{symbol} - Price Chart",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_rangeslider_visible=False
        )
        
        return fig
    
    @staticmethod
    def render_volume_chart(historical_data: List[Dict[str, Any]]) -> go.Figure:
        """Render volume chart"""
        df = pd.DataFrame(historical_data)
        
        if df.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=pd.to_datetime(df['date']),
            y=df['volume'],
            marker_color='#4ECDC4',
            opacity=0.7,
            name='Volume'
        ))
        
        fig.update_layout(
            title="Trading Volume",
            xaxis_title="Date",
            yaxis_title="Volume",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def render_market_overview(market_data: List[Dict[str, Any]]) -> go.Figure:
        """Render market overview chart"""
        df = pd.DataFrame(market_data)
        
        if df.empty:
            return go.Figure()
        
        # Sort by change percentage
        df = df.sort_values('change_percent', ascending=True)
        
        # Color based on performance
        colors = ['#00D4AA' if change >= 0 else '#FF6B6B' for change in df['change_percent']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df['symbol'],
            y=df['change_percent'],
            marker_color=colors,
            text=[f"{pct:+.1f}%" for pct in df['change_percent']],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>' +
                          'Change: %{y:.2f}%<br>' +
                          '<extra></extra>'
        ))
        
        fig.update_layout(
            title="Market Overview - Daily Performance",
            xaxis_title="Stock Symbol",
            yaxis_title="Change (%)",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
        
        return fig
    
    @staticmethod
    def render_sector_performance(sector_data: List[Dict[str, Any]]) -> go.Figure:
        """Render sector performance chart"""
        df = pd.DataFrame(sector_data)
        
        if df.empty:
            return go.Figure()
        
        # Sort by performance
        df = df.sort_values('change_percent', ascending=True)
        
        colors = ['#00D4AA' if change >= 0 else '#FF6B6B' for change in df['change_percent']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df['sector'],
            x=df['change_percent'],
            orientation='h',
            marker_color=colors,
            text=[f"{pct:+.1f}%" for pct in df['change_percent']],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Sector Performance",
            xaxis_title="Change (%)",
            yaxis_title="Sector",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False,
            height=500
        )
        
        return fig
    
    @staticmethod
    def render_market_filters() -> Dict[str, Any]:
        """Render market filter controls"""
        with st.sidebar:
            st.header("📊 Market Filters")
            
            # Symbol selection
            symbols = st.multiselect(
                "Select Symbols",
                options=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA'],
                default=['AAPL', 'MSFT', 'GOOGL'],
                help="Select stocks to analyze"
            )
            
            # Time period
            time_period = st.selectbox(
                "Time Period",
                options=["1D", "5D", "1M", "3M", "6M", "1Y", "2Y"],
                index=5,  # Default to 1Y
                help="Select time period for analysis"
            )
            
            # Market cap filter
            market_cap_range = st.slider(
                "Market Cap Range (Billions)",
                min_value=0,
                max_value=5000,
                value=(100, 3000),
                help="Filter by market capitalization"
            )
            
            # Sector filter
            sectors = st.multiselect(
                "Sectors",
                options=['Technology', 'Healthcare', 'Financial Services', 'Consumer Discretionary'],
                default=[],
                help="Filter by sector"
            )
            
            return {
                'symbols': symbols,
                'time_period': time_period,
                'market_cap_range': market_cap_range,
                'sectors': sectors
            }
    
    @staticmethod
    def render_market_summary(market_summary: Dict[str, Any]) -> None:
        """Render market summary metrics"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            sentiment_color = {
                'Bullish': '#00D4AA',
                'Bearish': '#FF6B6B',
                'Neutral': '#4ECDC4'
            }.get(market_summary.get('market_sentiment', 'Neutral'), '#4ECDC4')
            
            st.markdown(f"""
            <div style="text-align: center;">
                <h3 style="color: {sentiment_color};">
                    {market_summary.get('market_sentiment', 'Neutral')}
                </h3>
                <p>Market Sentiment</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric(
                "Volatility",
                market_summary.get('volatility_level', 'Medium'),
                help="Current market volatility level"
            )
        
        with col3:
            st.metric(
                "Advancing Sectors",
                f"{market_summary.get('advancing_sectors', 0)}/{market_summary.get('advancing_sectors', 0) + market_summary.get('declining_sectors', 0)}",
                help="Sectors with positive performance"
            )
        
        with col4:
            total_cap = market_summary.get('total_market_cap', 0)
            st.metric(
                "Total Market Cap",
                f"${total_cap:,.0f}B",
                help="Total market capitalization"
            )

# Create instance for export
market_component = MarketComponent()
