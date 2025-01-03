import streamlit as st
import numpy as np

def calculate_var(data, confidence_level=0.95):
    sorted_returns = np.sort(data)
    index = int((1 - confidence_level) * len(sorted_returns))
    return sorted_returns[index]

def display():
    st.title("Value at Risk (VaR)")
    st.write("Calculate and analyze Value at Risk for your portfolio.")

    # Simulate portfolio returns
    simulated_returns = np.random.randn(1000) / 100  # Simulated daily returns

    confidence_level = st.slider("Confidence Level", 0.90, 0.99, 0.95)
    var = calculate_var(simulated_returns, confidence_level)

    st.write(f"At {confidence_level*100}% confidence level, your daily VaR is: {var:.2%}")
