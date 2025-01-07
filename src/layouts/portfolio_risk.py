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


def display(portfolio_df):
    """
    Perform portfolio risk analysis for the given portfolio DataFrame.

    :param portfolio_df: DataFrame containing portfolio with 'Asset' and 'Weight' columns.
    """
    st.title("Portfolio Risk Analysis")

    # Validate the portfolio
    if portfolio_df["Weight"].sum() != 1.0:
        st.error("The weights must sum to 1.0.")
        return

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
