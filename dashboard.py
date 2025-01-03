import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Title and description
st.title("Market Risk Dashboard - Market Data and Trends")
st.write("Analyze market trends with historical data and visualizations.")

# Sidebar for user inputs
st.sidebar.header("Market Data Selection")
selected_asset = st.sidebar.selectbox(
    "Select an Index/Asset:",
    options=["^GSPC", "^IXIC", "^DJI", "TSLA", "AAPL"],
    format_func=lambda x: {
        "^GSPC": "S&P 500",
        "^IXIC": "NASDAQ",
        "^DJI": "Dow Jones",
        "TSLA": "Tesla",
        "AAPL": "Apple"
    }.get(x, x)
)
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-01-01"))

# Fetch market data
data = yf.download(selected_asset, start=start_date, end=end_date, auto_adjust=True)

if data.empty:
    st.error("No data available for the selected asset and date range. Please adjust your selection.")
else:
    # Display fetched data
    st.write(f"Data for {selected_asset} from {start_date} to {end_date}")
    st.dataframe(data)

    # Line chart for closing price
    st.subheader("Closing Price Trend")
    line_fig = px.line(data.reset_index(), x="Date", y="Close", title=f"{selected_asset} Closing Price")
    st.plotly_chart(line_fig)

    # Candlestick chart
    st.subheader("Candlestick Chart")
    candlestick_fig = go.Figure(
        data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )]
    )
    candlestick_fig.update_layout(title=f"{selected_asset} Candlestick Chart", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(candlestick_fig)

    # Heatmap of dummy sector data
    st.subheader("Sector Performance Heatmap")
    heatmap_data = pd.DataFrame({
        "Sector": ["Tech", "Energy", "Healthcare", "Finance", "Consumer"],
        "Performance": [0.12, -0.05, 0.08, -0.02, 0.03]
    })
    heatmap_fig = px.imshow(
        heatmap_data.set_index("Sector").T,
        title="Sector Performance Heatmap",
        labels=dict(x="Sector", y="Metric", color="Performance"),
        color_continuous_scale="RdYlGn"
    )
    st.plotly_chart(heatmap_fig)
