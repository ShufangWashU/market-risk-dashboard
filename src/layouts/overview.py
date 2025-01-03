import streamlit as st

def display():
    st.title("Home / Overview")
    st.write("Welcome to the Market Risk Dashboard!")
    st.write("Navigate through the tabs to explore market trends, risk analysis, and more.")
    
    # Add some summary metrics as placeholders
    st.metric("Portfolio VaR", "5%", delta="-0.1%")
    st.metric("S&P 500 Volatility", "12%", delta="0.5%")
    st.metric("Freshpet Volatility", "15%", delta="1.2%")

    st.write("Use the sidebar to switch between tabs.")
