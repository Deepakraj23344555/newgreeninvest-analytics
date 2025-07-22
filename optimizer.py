from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.expected_returns import mean_historical_return
import pandas as pd

def optimize_portfolio(esg_data, min_esg, max_carbon, risk_level):
    # Load historical price data
    price_df = pd.read_csv("data/sample_prices.csv", index_col=0, parse_dates=True)

    # Filter stocks based on ESG and carbon constraints
    filtered = esg_data[
        (esg_data['ESG Score'] >= min_esg) & 
        (esg_data['Carbon Footprint'] <= max_carbon)
    ]

    tickers = filtered['Ticker'].tolist()

    # Calculate expected returns and covariance matrix
    mu = mean_historical_return(price_df[tickers])
    S = CovarianceShrinkage(price_df[tickers]).ledoit_wolf()

    # Initialize Efficient Frontier optimizer
    ef = EfficientFrontier(mu, S)

    # Optimize based on risk appetite
    if risk_level == "High":
        weights = ef.max_sharpe()
    else:
        weights = ef.min_volatility()

    cleaned_weights = ef.clean_weights()

    # Prepare portfolio DataFrame with weights and ESG info
    portfolio_df = pd.DataFrame({
        "Ticker": list(cleaned_weights.keys()),
        "Weight": list(cleaned_weights.values())
    })

    portfolio_df = portfolio_df.merge(esg_data, on="Ticker")

    performance = {
        "return": ef.portfolio_performance()[0] * 100,  # Convert to %
        "carbon": (portfolio_df["Weight"] * portfolio_df["Carbon Footprint"]).sum()
    }

    return cleaned_weights, performance, portfolio_df
