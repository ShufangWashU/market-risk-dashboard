import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Title and description
st.title("Market Risk Dashboard")
st.write("Analyze and visualize the market risk and S&P 500.")

# Sidebar for user inputs
ticker = st.sidebar.text_input("Enter stock ticker (e.g., FRPT)", value="FRPT")
start_date = st.sidebar.date_input("Start Date", value="2015-01-01")
end_date = st.sidebar.date_input("End Date", value="2023-12-31")

# Convert date inputs to string format for yfinance
start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

st.write(f"Analyzing data for {ticker} from {start_date} to {end_date}.")

# Fetch stock data
data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

# Handle multi-level columns by dropping ticker level if present
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)

# Display fetched data
st.write(f"Data for {ticker}")
st.dataframe(data)

# Plot adjusted closing price
st.line_chart(data['Adj Close'])
st.write("Adjusted Closing Price Over Time")

# Calculate daily returns and rolling volatility
data['Daily Return'] = data['Adj Close'].pct_change()
data['Volatility'] = data['Daily Return'].rolling(window=30).std()

# Plot rolling volatility
st.line_chart(data['Volatility'])
st.write("30-Day Rolling Volatility")





# Add VaR calculation
def calculate_var(data, confidence_level=0.95):
    """
    Calculate the historical Value at Risk (VaR).
    """
    daily_returns = data['Daily Return'].dropna()  # Remove NaN values
    var = np.percentile(daily_returns, (1 - confidence_level) * 100)
    return var

# Confidence level input
confidence_level = st.sidebar.slider("Confidence Level (%)", min_value=90, max_value=99, value=95, step=1) / 100

# Display VaR
var = calculate_var(data, confidence_level=confidence_level)
st.write(f"Historical VaR ({int(confidence_level * 100)}% confidence): {var:.2%}")




def parametric_var(data, confidence_level=0.95, time_period=1):
    """
    Calculate parametric Value at Risk (VaR).
    """
    mean_return = data['Daily Return'].mean()
    std_dev = data['Daily Return'].std()
    z_score = np.abs(np.percentile([0, 1], (1 - confidence_level) * 100))
    var = z_score * std_dev * np.sqrt(time_period)
    return var

param_var = parametric_var(data, confidence_level=confidence_level)
st.write(f"Parametric VaR ({int(confidence_level * 100)}% confidence): {param_var:.2%}")







def calculate_cvar(data, confidence_level=0.95):
    """
    Calculate the Conditional Value at Risk (CVaR).
    """
    daily_returns = data['Daily Return'].dropna()
    var_threshold = np.percentile(daily_returns, (1 - confidence_level) * 100)
    cvar = daily_returns[daily_returns <= var_threshold].mean()
    return cvar

cvar = calculate_cvar(data, confidence_level=confidence_level)
st.write(f"Conditional VaR ({int(confidence_level * 100)}% confidence): {cvar:.2%}")



def monte_carlo_var(data, confidence_level=0.95, num_simulations=10000, time_horizon=1):
    """
    Monte Carlo simulation for Value at Risk (VaR).
    """
    mean_return = data['Daily Return'].mean()
    std_dev = data['Daily Return'].std()
    simulated_returns = np.random.normal(mean_return, std_dev, num_simulations)
    var = np.percentile(simulated_returns, (1 - confidence_level) * 100)
    return var

monte_carlo_var_value = monte_carlo_var(data, confidence_level=confidence_level)
st.write(f"Monte Carlo VaR ({int(confidence_level * 100)}% confidence): {monte_carlo_var_value:.2%}")
