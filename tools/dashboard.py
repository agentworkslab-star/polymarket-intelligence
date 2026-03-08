#!/usr/bin/env python3
"""
📊 Polymarket Dashboard - FREE Version
Streamlit-based dashboard for monitoring markets
Author: Agent Claw 🦾
Date: 2026-03-08
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import glob

# Page config
st.set_page_config(
    page_title="Polymarket Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 10%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .alert-high {
        background-color: #ff4444;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    .alert-medium {
        background-color: #ffbb33;
        color: black;
        padding: 10px;
        border-radius: 5px;
    }
    .alert-low {
        background-color: #00C851;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎯 Polymarket Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.header("🔧 Filters")
st.sidebar.markdown("---")

# Category filter
categories = ["All", "Politics", "Crypto", "Sports", "Geopolitics", "Finance", "Entertainment"]
selected_category = st.sidebar.selectbox("Category", categories)

# Timeframe filter
timeframes = ["24h", "7d", "30d", "All"]
selected_timeframe = st.sidebar.selectbox("Timeframe", timeframes)

# Refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")

# Load data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_market_data():
    """Load latest market data from CSV files"""
    csv_files = glob.glob("data/markets/scrape_*.csv")
    
    if not csv_files:
        return pd.DataFrame()
    
    latest_file = max(csv_files)
    df = pd.read_csv(latest_file)
    
    # Add category based on keywords
    df['Category'] = df['title'].apply(lambda x: 
        'Politics' if any(word in x.lower() for word in ['iran', 'election', 'political']) else
        'Crypto' if any(word in x.lower() for word in ['btc', 'bitcoin', 'crypto']) else
        'Sports' if any(word in x.lower() for word in ['nba', 'f1', 'football']) else
        'Other'
    )
    
    return df

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_all_data():
    """Load all historical data"""
    csv_files = glob.glob("data/markets/scrape_*.csv")
    
    if not csv_files:
        return pd.DataFrame()
    
    all_data = []
    for file in sorted(csv_files)[-10:]:  # Last 10 files
        df = pd.read_csv(file)
        all_data.append(df)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

# Load data
df = load_market_data()
historical_df = load_all_data()

# Sidebar stats
if not df.empty:
    st.sidebar.metric("Total Markets", len(df))
    st.sidebar.metric("Last Update", df['timestamp'].iloc[-1] if 'timestamp' in df.columns else "N/A")
    
    avg_prob = df['yes_price'].mean() * 100 if 'yes_price' in df.columns else 0
    st.sidebar.metric("Avg Probability", f"{avg_prob:.1f}%")
else:
    st.sidebar.warning("No data available")

# Main content
if df.empty:
    st.warning("📭 No market data available. Run scraper.py first!")
    
    st.markdown("### 🚀 Quick Start")
    st.code("python tools/scraper.py", language="bash")
    st.markdown("Then refresh this page.")
else:
    # Key Metrics
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Markets",
            value=len(df),
            delta="Live"
        )
    
    with col2:
        avg_yes = df['yes_price'].mean() * 10 if 'yes_price' in df.columns else 0
        st.metric(
            label="Avg Yes Probability",
            value=f"{avg_yes:.1f}%",
            delta=f"{avg_yes - 50:.1f}%"
        )
    
    with col3:
        total_vol = df['volume_24h'].sum() if 'volume_24h' in df.columns else 0
        st.metric(
            label="Total Volume (24h)",
            value=f"${total_vol:,.0f}",
            delta="24h"
        )
    
    with col4:
        total_liq = df['liquidity'].sum() if 'liquidity' in df.columns else 0
        st.metric(
            label="Total Liquidity",
            value=f"${total_liq:,.0f}",
            delta="Available"
        )
    
    st.markdown("---")
    
    # Market Data Table
    st.markdown("### 📊 Market Data")
    
    # Display table
    display_cols = ['title', 'yes_price', 'no_price', 'volume_24h', 'liquidity', 'timestamp']
    available_cols = [col for col in display_cols if col in df.columns]
    
    if available_cols:
        # Format for display
        display_df = df[available_cols].copy()
        
        # Rename columns
        column_names = {
            'title': 'Market',
            'yes_price': 'Yes Price',
            'no_price': 'No Price',
            'volume_24h': '24h Volume',
            'liquidity': 'Liquidity',
            'timestamp': 'Last Update'
        }
        display_df = display_df.rename(columns=column_names)
        
        # Format numbers
        if 'Yes Price' in display_df.columns:
            display_df['Yes Price'] = display_df['Yes Price'].apply(lambda x: f"${x:.2f}")
        if 'No Price' in display_df.columns:
            display_df['No Price'] = display_df['No Price'].apply(lambda x: f"${x:.2f}")
        if '24h Volume' in display_df.columns:
            display_df['24h Volume'] = display_df['24h Volume'].apply(lambda x: f"${x:,.0f}")
        if 'Liquidity' in display_df.columns:
            display_df['Liquidity'] = display_df['Liquidity'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(display_df, width="stretch", hide_index=True)
    else:
        st.warning("No columns available for display")
    
    st.markdown("---")
    
    # Charts
    st.markdown("### 📉 Charts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'yes_price' in df.columns:
            st.markdown("#### Probability Distribution")
            
            fig = px.histogram(
                df,
                x='yes_price',
                nbins=20,
                title='Probability Distribution',
                labels={'yes_price': 'Yes Probability'},
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width="stretch")
    
    with col2:
        if 'volume_24h' in df.columns:
            st.markdown("#### Volume by Market")
            
            fig = px.bar(
                df.head(10),
                x='title',
                y='volume_24h',
                title='Top 10 Markets by Volume',
                labels={'title': 'Market', 'volume_24h': 'Volume'},
                color='volume_24h',
                color_continuous_scale='Reds'
            )
            fig.update_layout(showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig, width="stretch")
    
    # Historical Trends
    if not historical_df.empty and 'timestamp' in historical_df.columns:
        st.markdown("---")
        st.markdown("### 📈 Historical Trends")
        
        if 'yes_price' in historical_df.columns:
            fig = px.line(
                historical_df,
                x='timestamp',
                y='yes_price',
                title='Probability Over Time',
                labels={'timestamp': 'Time', 'yes_price': 'Yes Probability'}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width="stretch")
    
    # Alerts Section
    st.markdown("---")
    st.markdown("### 🚨 Recent Alerts")
    
    if 'yes_price' in df.columns:
        # Find significant movements (placeholder logic)
        high_prob = df[df['yes_price'] > 0.7]
        low_prob = df[df['yes_price'] < 0.3]
        
        if not high_prob.empty:
            st.markdown("#### 🔴 High Probability Markets (>70%)")
            for _, row in high_prob.iterrows():
                st.markdown(f"""
                <div class="alert-high">
                <b>{row['title']}</b><br>
                Probability: {row['yes_price']*100:.1f}%
                </div>
                """, unsafe_allow_html=True)
        
        if not low_prob.empty:
            st.markdown("#### 🟢 Low Probability Markets (<30%)")
            for _, row in low_prob.iterrows():
                st.markdown(f"""
                <div class="alert-low">
                <b>{row['title']}</b><br>
                Probability: {row['yes_price']*100:.1f}%
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #88;">
    <p>🎯 Polymarket Intelligence Dashboard | Updated: {time}</p>
    <p>Built with Streamlit | Data Source: Polymarket.com</p>
</div>
""".format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

# Auto-refresh option
if st.checkbox("⏱️ Auto-refresh every 60 seconds"):
    import time
    time.sleep(60)
    st.rerun()
