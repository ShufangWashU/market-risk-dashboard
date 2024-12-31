# Market Risk Dashboard

## Overview
The **Market Risk Dashboard** is an interactive tool developed using Python and Streamlit to analyze and visualize the market risks of selected stocks. This dashboard provides valuable risk metrics, including historical Value at Risk (VaR), parametric VaR, conditional VaR (CVaR), and Monte Carlo VaR. Additionally, it features rolling volatility analysis and dynamic visualizations to assist in assessing the financial risk associated with an asset.

---

## Features
1. **Fetch Stock Data**:
   - Use `yfinance` to fetch historical stock data.
   - Supports user-specified stock tickers, start dates, and end dates.

2. **Visualizations**:
   - Adjusted Closing Price over time.
   - Rolling Volatility (30-day standard deviation).

3. **Risk Metrics**:
   - **Historical VaR**: Based on historical daily returns.
   - **Parametric VaR**: Uses mean and standard deviation of returns with an assumption of normal distribution.
   - **Conditional VaR (CVaR)**: Expected loss beyond the VaR threshold.
   - **Monte Carlo VaR**: Simulated returns to estimate potential losses.

4. **User Inputs**:
   - Customizable confidence levels for VaR (90% to 99%).

---

## How to Run

### Prerequisites
1. Install Python (>=3.8).
2. Install dependencies using `pip`:
   ```bash
   pip install streamlit yfinance pandas numpy
   ```

### Run the Application
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd market-risk-dashboard
   ```

2. Launch the dashboard:
   ```bash
   streamlit run dashboard.py
   ```

3. Open the URL displayed in the terminal (default: `http://localhost:8501`) to access the dashboard in your browser.

---

## File Structure
```plaintext
market-risk-dashboard/
├── dashboard.py       # Main script for the dashboard
├── README.md          # Project documentation
└── requirements.txt   # Python dependencies
```

---

## How It Works
### Input Parameters
- **Stock Ticker**: Enter the stock symbol (e.g., `AAPL`, `FRPT`).
- **Date Range**: Specify the start and end dates for historical data analysis.
- **Confidence Level**: Adjust the confidence level for VaR calculations.

### Calculations
1. **Daily Returns**:
   - Percentage change in Adjusted Close prices.

2. **Rolling Volatility**:
   - 30-day rolling standard deviation of daily returns.

3. **Value at Risk (VaR)**:
   - **Historical VaR**: Based on historical returns.
   - **Parametric VaR**: Assumes normal distribution.
   - **Conditional VaR (CVaR)**: Average loss beyond VaR.
   - **Monte Carlo VaR**: Simulated returns to estimate losses.

---

## Next Steps
1. Add portfolio risk analysis for multi-asset portfolios.
2. Implement efficient frontier and portfolio optimization.
3. Deploy the dashboard online using Streamlit Cloud