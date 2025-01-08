import streamlit as st

def display():
    # Add custom CSS for increased line spacing
    st.markdown(
        """
        <style>
        .stMarkdown p {
            line-height: 1.8; /* Adjust this value to increase/decrease line spacing */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Home / Overview")
    st.write("### Welcome to the Market Risk Dashboard!")
    st.write("""
    This dashboard is designed to help you visualize and analyze various aspects of market risk. 
    Follow these steps to make the most of it:
    1. Use the sidebar to navigate through the different tabs:
        - **Market Data and Trends**: Explore historical and real-time market data.
        - **Value at Risk (VaR)**: Analyze portfolio risk using VaR methods.
        - **Monte Carlo Simulations**: Run simulations to predict potential outcomes.
        - **GARCH Modeling**: Study volatility trends using advanced models.
        - **Alerts and Monitoring**: Set up custom alerts and monitor market risks.
    2. Customize inputs such as stock symbols, time ranges, and parameters as needed.
    3. Visualize interactive plots and download results for further analysis.
    """)
    
    st.write("Feel free to reach out for questions or feedback:")
    st.markdown("- **Email**: [shufang@wustl](mailto:shufang@wustl)")
    st.markdown("- **GitHub Repository**: [Market Risk Dashboard](https://github.com/ShufangWashU/market-risk-dashboard)")
    
    st.write("Thank you for using the Market Risk Dashboard!")
