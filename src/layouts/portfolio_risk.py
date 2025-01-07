import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px


# Fetch historical data (cached)
@st.cache_data
def fetch_data(tickers, period="1y"):
    return yf.download(tickers, period=period, auto_adjust=False)["Adj Close"]


# Calculate portfolio returns (cached)
@st.cache_data
def calculate_portfolio_returns(data, weights):
    returns = data.pct_change()
    portfolio_returns = (returns * weights).sum(axis=1)
    return portfolio_returns


def display():
    st.title("Portfolio Risk Analysis")

    # Sidebar: Portfolio Input
    st.sidebar.header("Portfolio Input")

    # Initialize session state for portfolio
    if "portfolio" not in st.session_state:
        st.session_state["portfolio"] = [{"Asset": "", "Weight": 1.0}]

    # Add stock input dynamically
    def add_stock():
        st.session_state["portfolio"].append({"Asset": "", "Weight": 0.0})

    # Remove the last stock dynamically
    def remove_stock():
        if len(st.session_state["portfolio"]) > 1:
            st.session_state["portfolio"].pop()

    # Display stocks in the sidebar
    for i, stock in enumerate(st.session_state["portfolio"]):
        st.sidebar.text_input(f"Ticker {i + 1}:", value=stock["Asset"], key=f"asset_{i}")
        st.sidebar.number_input(
            f"Weight {i + 1}:", min_value=0.0, max_value=1.0, step=0.01, value=stock["Weight"], key=f"weight_{i}"
        )

    # Buttons to add/remove stocks
    st.sidebar.button("Add Stock", on_click=add_stock)
    st.sidebar.button("Remove Stock", on_click=remove_stock)

    # Get the current portfolio
    portfolio_df = pd.DataFrame(
        [{"Asset": st.session_state[f"asset_{i}"], "Weight": st.session_state[f"weight_{i}"]} for i in range(len(st.session_state["portfolio"]))]
    )

    # Validate the portfolio
    if portfolio_df["Weight"].sum() != 1.0:
        st.sidebar.error("The weights must sum to 1.0.")
    else:
        st.sidebar.success("Portfolio is valid!")

    # Perform analysis only if portfolio is valid
    if portfolio_df["Weight"].sum() == 1.0:
        # Fetch data
        tickers = portfolio_df["Asset"].tolist()
        weights = portfolio_df["Weight"].tolist()

        if len(tickers) > 0 and all(tickers):
            data = fetch_data(tickers)

            # Single stock analysis
            if len(tickers) == 1:
                st.header(f"Performance of {tickers[0]}")
                st.line_chart(data)

            # Portfolio analysis
            elif len(tickers) > 1:
                # Portfolio Returns
                portfolio_returns = calculate_portfolio_returns(data, weights)
                cumulative_returns = (1 + portfolio_returns).cumprod()

                st.header("Portfolio Performance")
                st.line_chart(cumulative_returns)

                # Risk Decomposition
                volatilities = data.pct_change().std() * np.sqrt(252)  # Annualized volatility
                risk_contributions = volatilities * weights
                risk_contributions_percentage = (risk_contributions / risk_contributions.sum()) * 100
                risk_df = pd.DataFrame({"Asset": tickers, "Risk Contribution (%)": risk_contributions_percentage})
                st.subheader("Risk Decomposition")
                st.dataframe(risk_df)

                # Risk Pie Chart
                fig = px.pie(risk_df, names="Asset", values="Risk Contribution (%)", title="Risk Contribution by Asset")
                st.plotly_chart(fig)

                # Correlation Matrix
                st.subheader("Correlation Matrix")
                corr_matrix = data.pct_change().corr()
                fig = px.imshow(
                    corr_matrix,
                    labels=dict(x="Assets", y="Assets", color="Correlation"),
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    color_continuous_scale="RdBu",
                    zmin=-1,
                    zmax=1,
                )
                st.plotly_chart(fig)

                # Portfolio VaR and PVaR
                st.header("Portfolio VaR and Parametric VaR")
                confidence_level = st.slider("Confidence Level (%)", 90, 99, 95)
                var_percentile = 100 - confidence_level

                # Historical VaR
                historical_var = np.percentile(portfolio_returns, var_percentile)

                # Parametric VaR
                portfolio_std = portfolio_returns.std()
                z_score = abs(np.percentile(np.random.normal(0, 1, 10000), var_percentile / 100))
                parametric_var = z_score * portfolio_std

                st.subheader("VaR Results")
                st.write(f"Historical VaR: **{historical_var:.4f}**")
                st.write(f"Parametric VaR: **{parametric_var:.4f}**")
