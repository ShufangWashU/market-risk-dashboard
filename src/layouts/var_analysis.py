import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def calculate_var(data, confidence_level=0.95):
    sorted_returns = np.sort(data)
    index = int((1 - confidence_level) * len(sorted_returns))
    return sorted_returns[index]

def calculate_parametric_var(mean, std_dev, confidence_level=0.95):
    z_score = np.abs(np.percentile(np.random.randn(100000), (1 - confidence_level) * 100))
    return mean - z_score * std_dev

def monte_carlo_var(data, confidence_level=0.95, simulations=10000):
    simulated_returns = np.random.choice(data, size=simulations, replace=True)
    return calculate_var(simulated_returns, confidence_level)

def calculate_cvar(data, confidence_level=0.95):
    var = calculate_var(data, confidence_level)
    return data[data <= var].mean()

def display(portfolio_df, start_date, end_date):
    st.title("3. VaR Analysis")
    st.write("Performing Value at Risk (VaR) analysis for your portfolio.")

    # Validate portfolio
    if portfolio_df.empty or portfolio_df["Asset"].str.strip().eq("").any():
        st.warning("Please define a valid portfolio in the sidebar.")
        return

    # Select stock from portfolio
    focused_stock = st.selectbox(
        "Select a stock from your portfolio for VaR analysis:",
        portfolio_df["Asset"].tolist()
    )

    # Fetch data
    try:
        df = yf.download(focused_stock, start=start_date, end=end_date, auto_adjust=False)
        df['Daily Returns'] = df['Adj Close'].pct_change().dropna()

        if df.empty:
            st.error("No data available for the selected stock and date range.")
            return
        
        # Input confidence level
        confidence_level = st.slider("Confidence Level", 0.90, 0.99, 0.95)

        # Calculations
        daily_returns = df['Daily Returns'].dropna().values
        mean_return = np.mean(daily_returns)
        std_dev = np.std(daily_returns)

        var = calculate_var(daily_returns, confidence_level)
        parametric_var = calculate_parametric_var(mean_return, std_dev, confidence_level)
        monte_carlo_var_value = monte_carlo_var(daily_returns, confidence_level)
        cvar = calculate_cvar(daily_returns, confidence_level)

        # Display results
        st.write(f"**VaR at {confidence_level*100}% confidence level:** {var:.2%}")
        st.write(f"**Parametric VaR:** {parametric_var:.2%}")
        st.write(f"**Monte Carlo VaR:** {monte_carlo_var_value:.2%}")
        st.write(f"**CVaR (Expected Shortfall):** {cvar:.2%}")

        # Visualization
        st.write("Return Distribution:")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(daily_returns, bins=50, alpha=0.7, color='gray', label='Daily Returns')
        ax.axvline(x=var, color='red', linestyle='dashed', linewidth=2, label='VaR')
        ax.axvline(x=cvar, color='blue', linestyle='dashed', linewidth=2, label='CVaR')
        ax.set_title(f"Return Distribution with VaR and CVaR ({confidence_level*100}% Confidence Level)")
        ax.set_xlabel("Daily Returns")
        ax.set_ylabel("Frequency")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")
