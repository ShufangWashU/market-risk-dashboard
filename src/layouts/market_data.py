import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import streamlit as st
import yfinance as yf
import pandas as pd

@st.cache_data
def fetch_stock_data(stock, start_date, end_date, granularity):
    """
    Fetch historical stock data using yfinance.
    :param stock: Stock ticker (string)
    :param start_date: Start date for historical data (datetime)
    :param end_date: End date for historical data (datetime)
    :param granularity: Data granularity (Daily, Weekly, Monthly)
    :return: Pandas DataFrame with stock data
    """
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
    
def display(portfolio_df, focused_stock, start_date, end_date, granularity):
    st.title("2. Market Data and Trends")
    st.write("Analyze and visualize market data for your portfolio.")

    # Ensure the portfolio is valid
    if portfolio_df.empty or portfolio_df["Asset"].str.strip().eq("").any():
        st.warning("Please define a valid portfolio in the sidebar.")
        return

    # Fetch and visualize data for the focused stock
    if focused_stock:
        st.subheader(f"Focused Analysis: {focused_stock}")

        # Fetch Data
        data = fetch_stock_data(focused_stock, start_date, end_date, granularity)
        if data is None:
            st.warning(f"No data found for {focused_stock.upper()} between {start_date} and {end_date}.")
            return
        elif isinstance(data, str):
            st.error(f"Error fetching data for {focused_stock}: {data}")
            return

        # Stock Data Table
        with st.expander(f"Data for {focused_stock.upper()}"):
            st.dataframe(data)
            csv_data = data.to_csv().encode('utf-8')
            st.download_button(f"Download {focused_stock.upper()} Data as CSV", csv_data, f"{focused_stock}_data.csv", "text/csv")

        # Candlestick Chart
        with st.expander(f"{focused_stock.upper()} Price Movement Analysis"):
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
                candlestick.update_layout(title=f"{focused_stock.upper()} Candlestick Chart", xaxis_title="Date", yaxis_title="Price")
                st.plotly_chart(candlestick, use_container_width=True)
            else:
                st.warning("Required columns for candlestick chart not found.")

        # Cumulative Returns
        with st.expander(f"{focused_stock.upper()} Cumulative Returns"):
            st.write("Explore cumulative returns to assess overall performance.")
            close_col = next((col for col in data.columns if 'close' in col.lower()), None)
            if close_col:
                data['Daily Return'] = data[close_col].pct_change()
                data['Cumulative Return'] = (1 + data['Daily Return']).cumprod()
                st.area_chart(data['Cumulative Return'])
            else:
                st.warning("Close price column not found for cumulative returns.")

    else:
        st.warning("No stock selected for focused analysis.")
