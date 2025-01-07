import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def apply_scenario(returns, scenario_impact):
    """
    Apply a stress-testing scenario to portfolio returns.

    :param returns: Series of portfolio returns
    :param scenario_impact: Percentage impact for the scenario (e.g., -10 for a 10% drop)
    :return: Adjusted returns after applying the scenario
    """
    adjusted_returns = returns * (1 + scenario_impact / 100)
    return adjusted_returns


def display(portfolio_df, portfolio_returns):
    """
    Perform stress testing and scenario analysis for the given portfolio.

    :param portfolio_df: DataFrame containing portfolio with 'Asset' and 'Weight' columns
    :param portfolio_returns: Series of portfolio daily returns
    """
    st.title("Stress Testing and Scenario Analysis")

    # Validate inputs
    if portfolio_df.empty or portfolio_returns is None or portfolio_returns.empty:
        st.warning("Please ensure the portfolio is valid and returns are calculated.")
        return

    # Section 1: Introduction
    st.header("Introduction")
    st.write("""
        Stress testing and scenario analysis evaluate portfolio performance under extreme conditions.
        This helps identify vulnerabilities and improve risk management strategies.
    """)

    # Section 2: Predefined Scenarios
    st.header("Predefined Scenarios")
    predefined_scenarios = {
        "Interest Rate Hike": -10,  # -10% portfolio impact
        "Oil Price Shock": -8,     # -8% portfolio impact
        "Market Crash": -30        # -30% portfolio impact
    }

    selected_scenario = st.selectbox("Select a predefined scenario:", list(predefined_scenarios.keys()))

    if selected_scenario:
        scenario_impact = predefined_scenarios[selected_scenario]
        adjusted_returns = apply_scenario(portfolio_returns, scenario_impact)
        cumulative_returns = (1 + adjusted_returns).cumprod()

        st.write(f"**Selected Scenario:** {selected_scenario}")
        st.write(f"**Impact Applied:** {scenario_impact}%")

        # Visualization: Impact of the scenario
        st.header(f"Impact of {selected_scenario} on Portfolio Performance")
        st.line_chart(cumulative_returns)

    # Section 3: Custom Scenario Builder
    st.header("Custom Scenario Builder")
    custom_scenario_impact = st.slider("Define your custom scenario impact (%)", min_value=-50, max_value=50, value=0)

    if custom_scenario_impact != 0:
        custom_adjusted_returns = apply_scenario(portfolio_returns, custom_scenario_impact)
        custom_cumulative_returns = (1 + custom_adjusted_returns).cumprod()

        st.write(f"**Custom Scenario Impact Applied:** {custom_scenario_impact}%")

        # Visualization: Impact of the custom scenario
        st.header("Impact of Custom Scenario on Portfolio Performance")
        st.line_chart(custom_cumulative_returns)

    # Section 4: Summary and Insights
    st.header("Summary and Insights")
    st.write("""
        Stress testing results provide critical insights into how extreme conditions affect the portfolio.
        Consider rebalancing or hedging to mitigate identified risks.
    """)

    # Download Results
    st.header("Download Adjusted Returns")
    adjusted_data = pd.DataFrame({
        "Predefined Scenario Returns": cumulative_returns if selected_scenario else [],
        "Custom Scenario Returns": custom_cumulative_returns if custom_scenario_impact else []
    })
    st.download_button(
        label="Download Adjusted Returns (CSV)",
        data=adjusted_data.to_csv(index=False),
        file_name="stress_testing_results.csv",
        mime="text/csv"
    )
