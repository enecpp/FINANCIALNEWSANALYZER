"""
News Component
Streamlit components for displaying financial news
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List
import pandas as pd

class NewsComponent:
    """Component for rendering news-related UI elements"""
    
    @staticmethod
    def render_news_card(news_item: Dict[str, Any]) -> None:
        """Render a single news card"""
        sentiment_color = {
            'Positive': '#00D4AA',
            'Negative': '#FF6B6B',
            'Neutral': '#4ECDC4'
        }.get(news_item.get('sentiment', 'Neutral'), '#4ECDC4')
        
        with st.container():
            st.markdown(f"""
            <div style="
                background: var(--secondary-bg);
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid {sentiment_color};
                margin: 10px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            ">
                <h4 style="color: {sentiment_color}; margin: 0 0 10px 0;">
                    {news_item.get('headline', 'News Headline')}
                </h4>
                <p style="margin: 5px 0; color: #CCCCCC;">
                    <strong>Company:</strong> {news_item.get('company', 'N/A')} | 
                    <strong>Source:</strong> {news_item.get('source', 'N/A')} | 
                    <strong>Sentiment:</strong> {news_item.get('sentiment', 'N/A')}
                </p>
                <p style="margin: 5px 0; color: #FAFAFA;">
                    {news_item.get('summary', 'No summary available.')}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_sentiment_chart(sentiment_data: Dict[str, int]) -> go.Figure:
        """Render sentiment distribution chart"""
        fig = go.Figure(data=[
            go.Bar(
                x=list(sentiment_data.keys()),
                y=list(sentiment_data.values()),
                marker_color=['#00D4AA', '#FF6B6B', '#4ECDC4'],
                text=list(sentiment_data.values()),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="News Sentiment Distribution",
            xaxis_title="Sentiment",
            yaxis_title="Number of Articles",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def render_news_timeline(news_data: List[Dict[str, Any]]) -> go.Figure:
        """Render news timeline chart"""
        # Convert to DataFrame for easier processing
        df = pd.DataFrame(news_data)
        if 'published_at' in df.columns:
            df['date'] = pd.to_datetime(df['published_at']).dt.date
            timeline_data = df.groupby(['date', 'sentiment']).size().reset_index(name='count')
            
            fig = px.line(
                timeline_data, 
                x='date', 
                y='count', 
                color='sentiment',
                title="News Sentiment Timeline",
                color_discrete_map={
                    'Positive': '#00D4AA',
                    'Negative': '#FF6B6B',
                    'Neutral': '#4ECDC4'
                }
            )
            
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            return fig
        
        # Fallback empty chart
        return go.Figure()
    
    @staticmethod
    def render_news_filters() -> Dict[str, Any]:
        """Render news filter controls"""
        with st.sidebar:
            st.header("📰 News Filters")
            
            # Date range filter
            date_range = st.date_input(
                "Date Range",
                value=[pd.Timestamp.now() - pd.Timedelta(days=7), pd.Timestamp.now()],
                help="Select date range for news"
            )
            
            # Sentiment filter
            sentiment_filter = st.multiselect(
                "Sentiment",
                options=['Positive', 'Negative', 'Neutral'],
                default=['Positive', 'Negative', 'Neutral'],
                help="Filter by news sentiment"
            )
            
            # Source filter
            source_filter = st.multiselect(
                "News Sources",
                options=['Reuters', 'Bloomberg', 'CNBC', 'Financial Times', 'Wall Street Journal'],
                default=[],
                help="Filter by news source"
            )
            
            # Category filter
            category_filter = st.multiselect(
                "Categories",
                options=['Earnings', 'Product Launch', 'Market Analysis', 'Merger', 'Partnership'],
                default=[],
                help="Filter by news category"
            )
            
            return {
                'date_range': date_range,
                'sentiment': sentiment_filter,
                'sources': source_filter,
                'categories': category_filter
            }
    
    @staticmethod
    def render_news_summary(news_stats: Dict[str, Any]) -> None:
        """Render news summary metrics"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Articles",
                news_stats.get('total_articles', 0),
                help="Total number of news articles"
            )
        
        with col2:
            st.metric(
                "Avg Sentiment",
                f"{news_stats.get('average_sentiment', 0):.2f}",
                help="Average sentiment score (-1 to 1)"
            )
        
        with col3:
            st.metric(
                "Most Active Source",
                news_stats.get('most_active_source', 'N/A'),
                help="Source with most articles"
            )
        
        with col4:
            st.metric(
                "Dominant Category",
                news_stats.get('dominant_category', 'N/A'),
                help="Most common news category"
            )

# Create instance for export
news_component = NewsComponent()
