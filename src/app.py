import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from layouts import market_data, overview, var_analysis, portfolio_risk, stress_testing


# Global Inputs (Sidebar)
st.sidebar.header("Portfolio Inputs")

# Initialize session state for portfolio
if "portfolio" not in st.session_state:
    st.session_state["portfolio"] = [{"Asset": "FRPT", "Weight": 1.0}]  # Default single stock

# Add stock dynamically
def add_stock():
    st.session_state["portfolio"].append({"Asset": "", "Weight": 0.0})

# Remove stock dynamically
def remove_stock():
    if len(st.session_state["portfolio"]) > 1:
        st.session_state["portfolio"].pop()

# Display portfolio input fields
for i, stock in enumerate(st.session_state["portfolio"]):
    st.sidebar.text_input(f"Ticker {i + 1}:", value=stock["Asset"], key=f"asset_{i}")
    st.sidebar.number_input(
        f"Weight {i + 1}:", min_value=0.0, max_value=1.0, step=0.01, value=stock["Weight"], key=f"weight_{i}"
    )

# Buttons to add/remove stocks
st.sidebar.button("Add Stock", on_click=add_stock, key="add_stock_button")
st.sidebar.button("Remove Stock", on_click=remove_stock, key="remove_stock_button")

# Convert session state to portfolio DataFrame
portfolio_df = pd.DataFrame(
    [{"Asset": st.session_state[f"asset_{i}"], "Weight": st.session_state[f"weight_{i}"]} for i in range(len(st.session_state["portfolio"]))]
)

# Validate portfolio weights
if portfolio_df["Weight"].sum() != 1.0:
    st.sidebar.error("The weights must sum to 1.0.")
else:
    st.sidebar.success("Portfolio is valid!")

# Dropdown for selecting a stock from the portfolio
focused_stock = st.sidebar.selectbox(
    "Select a stock to focus on:", 
    portfolio_df["Asset"].tolist() if not portfolio_df.empty else [],
    key="focused_stock"
)

# Date Range and Granularity Inputs
start_date = st.sidebar.date_input("Select Start Date:", pd.to_datetime("2020-01-01"), key="start_date")
end_date = st.sidebar.date_input("Select End Date:", pd.to_datetime("2023-01-01"), key="end_date")
granularity = st.sidebar.selectbox("Select Data Granularity:", ["Daily", "Weekly", "Monthly"], key="granularity")

# Navigation
st.sidebar.title("Navigation")
selected_tab = st.sidebar.radio(
    "Choose a tab:",
    ["Overview", "Market Data and Trends", "VaR Analysis", "Portfolio Risk Analysis", "Stress Testing and Scenario Analysis"],
    key="navigation_tabs"
)

# Display Selected Tab
if selected_tab == "Overview":
    overview.display()
elif selected_tab == "Market Data and Trends":
    market_data.display(portfolio_df, focused_stock, start_date, end_date, granularity)
elif selected_tab == "VaR Analysis":
    var_analysis.display(portfolio_df, start_date, end_date)
elif selected_tab == "Portfolio Risk Analysis":
    portfolio_risk.display(portfolio_df)
elif selected_tab == "Stress Testing and Scenario Analysis":
    # Check if the portfolio is valid
    if portfolio_df.empty:
        st.warning("Please define a valid portfolio in the sidebar before performing stress testing.")
    elif portfolio_df["Weight"].sum() != 1.0:
        st.warning("The weights of your portfolio do not sum to 1.0. Please adjust them in the sidebar.")
    else:
        tickers = portfolio_df["Asset"].tolist()
        weights = portfolio_df["Weight"].tolist()
        try:
            data = portfolio_risk.fetch_data(tickers, period="1y")  # Use existing fetch_data function
            if data is not None and not data.empty:
                portfolio_returns = portfolio_risk.calculate_portfolio_returns(data, weights)
                stress_testing.display(portfolio_df, portfolio_returns)
            else:
                st.error("Failed to fetch data for the given tickers.")
        except Exception as e:
            st.error(f"Error fetching data or calculating returns: {e}")
