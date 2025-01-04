# pip install yahooquery

import feedparser
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Helper Function to Fetch News
def fetch_stock_news(stock):
    feed_url = f"https://news.google.com/rss/search?q={stock}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(feed_url)
    return [{"title": entry.title, "link": entry.link} for entry in feed.entries]

# Cached Function to Fetch Stock Data
@st.cache_data
def fetch_stock_data(stock, start_date, end_date, granularity):
    try:
        interval = {"Daily": "1d", "Weekly": "1wk", "Monthly": "1mo"}[granularity]
        data = yf.download(stock, start=start_date, end=end_date, interval=interval, auto_adjust=False)
        if data.empty:
            return None
        # Flatten Multi-Index if needed
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in data.columns]
        return data
    except Exception as e:
        return str(e)


# Display Function for Market Data and Trends
def display(stock, start_date, end_date, granularity):
    st.title("2. Market Data and Trends")
    st.write("Analyze and visualize market data with enhanced insights, interactive visualizations, and key metrics.")

    # Fetch Data
    data = fetch_stock_data(stock, start_date, end_date, granularity)
    if data is None:
        st.warning(f"No data found for {stock.upper()} between {start_date} and {end_date}.")
        return
    elif isinstance(data, str):
        st.error(f"Error fetching data: {data}")
        return

    # Stock Data Table
    with st.expander("2.1 Stock Data Table", expanded=True):
        st.write(f"Data for {stock.upper()}")
        st.dataframe(data)
        csv_data = data.to_csv().encode('utf-8')
        st.download_button("Download Data as CSV", csv_data, f"{stock}_data.csv", "text/csv")

    # Candlestick Chart
    with st.expander("2.2 Price Movement Analysis", expanded=True):
        st.write("Visualize detailed price movements with candlestick patterns.")
        open_col = next((col for col in data.columns if 'open' in col.lower()), None)
        high_col = next((col for col in data.columns if 'high' in col.lower()), None)
        low_col = next((col for col in data.columns if 'low' in col.lower()), None)
        close_col = next((col for col in data.columns if 'close' in col.lower()), None)

        if all([open_col, high_col, low_col, close_col]):
            candlestick = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data[open_col],
                high=data[high_col],
                low=data[low_col],
                close=data[close_col]
            )])
            candlestick.update_layout(title=f"{stock.upper()} Candlestick Chart", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(candlestick, use_container_width=True)
        else:
            st.warning("Required columns for candlestick chart not found.")

    # Cumulative Returns
    with st.expander("2.3 Cumulative Returns", expanded=False):
        st.write("Explore cumulative returns to assess overall performance.")
        close_col = next((col for col in data.columns if 'close' in col.lower()), None)
        if close_col:
            data['Daily Return'] = data[close_col].pct_change()
            data['Cumulative Return'] = (1 + data['Daily Return']).cumprod()
            st.area_chart(data['Cumulative Return'])
        else:
            st.warning("Close price column not found for cumulative returns.")

    # Histogram for Trading Volume
    with st.expander("2.4 Trading Volume Histogram", expanded=False):
        st.write("Visualize the distribution of trading volumes.")
        volume_col = next((col for col in data.columns if 'volume' in col.lower()), None)
        if volume_col:
            st.bar_chart(data[volume_col])
        else:
            st.warning("Volume column not found.")

    # Key Metrics
    with st.expander("2.5 Key Metrics", expanded=False):
        st.write("Summary of important metrics.")
        if close_col and volume_col:
            largest_change = data[close_col].max() - data[close_col].min()
            avg_volume = data[volume_col].mean()
            st.metric(label="Largest Price Change", value=f"{largest_change:.2f}")
            st.metric(label="Average Volume", value=f"{avg_volume:,.0f}")
        else:
            st.warning("Required columns for metrics not found.")

    # Fundamental Data
    with st.expander("2.6 Fundamental Data", expanded=False):
        st.write("Basic financial metrics for the stock.")
        ticker = yf.Ticker(stock)
        info = ticker.info
        fundamentals = {
            "P/E Ratio": info.get("forwardPE"),
            "EPS": info.get("trailingEps"),
            "Market Cap": info.get("marketCap"),
            "52 Week High": info.get("fiftyTwoWeekHigh"),
            "52 Week Low": info.get("fiftyTwoWeekLow")
        }
        st.table(pd.DataFrame.from_dict(fundamentals, orient="index", columns=["Value"]))

    # Latest News
    with st.expander("2.7 Latest News", expanded=False):
        st.write("Stay updated with the latest news related to this stock.")
        news_feed = fetch_stock_news(stock)
        if news_feed:
            for news_item in news_feed[:3]:
                st.markdown(f"""
                <div style="display: flex; align-items: center; background-color: #2b2b2b; padding: 15px; border-radius: 10px; border: 1px solid #444; margin-bottom: 10px;">
                    <a href="{news_item['link']}" target="_blank" style="text-decoration: none; color: #4CAF50; font-weight: bold; font-size: 1em;">
                        📰 {news_item['title']}
                    </a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write(f"No news available for {stock.upper()}.")

    # Data Update
    with st.expander("2.8 Data Update", expanded=False):
        st.write(f"Data last updated: {datetime.now()}")
        if st.button("Refresh Data"):
            st.experimental_rerun()
    
