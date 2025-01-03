import streamlit as st
from layouts import overview, market_data, var_analysis

# Create tabs for navigation
tab1, tab2, tab3 = st.tabs(["Home / Overview", "Market Data", "Value at Risk"])

# Define content for each tab
with tab1:
    overview.display()  # Call the function from layouts/overview.py

with tab2:
    market_data.display()  # Call the function from layouts/market_data.py

with tab3:
    var_analysis.display()  # Call the function from layouts/var_analysis.py
