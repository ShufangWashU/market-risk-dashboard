import streamlit as st
from layouts import market_data, overview, var_analysis, portfolio_risk
# Import necessary libraries
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime


# Global Inputs (Sidebar)
st.sidebar.header("Global Inputs")
stock = st.sidebar.text_input("Enter Stock Ticker (e.g., FRPT, AAPL):", "FRPT", key="stock_input")
start_date = st.sidebar.date_input("Select Start Date:", pd.to_datetime("2020-01-01"), key="start_date")
end_date = st.sidebar.date_input("Select End Date:", pd.to_datetime("2023-01-01"), key="end_date")
granularity = st.sidebar.selectbox("Select Data Granularity:", ["Daily", "Weekly", "Monthly"], key="granularity")

# Navigation
st.sidebar.title("Navigation")
selected_tab = st.sidebar.radio(
    "Choose a tab:",
    ["Overview", "Market Data & Trends", "VaR Analysis", "Portfolio Risk Analysis"]
)


# Display Selected Tab
if selected_tab == "Overview":
    overview.display()
elif selected_tab == "Market Data and Trends":
    market_data.display(stock, start_date, end_date, granularity)
elif selected_tab == "VaR Analysis":
    var_analysis.display(stock, start_date, end_date)  
elif selected_tab == "Portfolio Risk Analysis":
    portfolio_risk.display()

