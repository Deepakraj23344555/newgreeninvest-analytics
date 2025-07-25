# optimizer.py

import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns

def optimize_portfolio(esg_data, esg_min, max_carbon, risk_appetite):
    """
    Optimize portfolio based on ESG and carbon footprint constraints and risk appetite.
    
    Parameters:
        esg_data (pd.DataFrame): ESG data containing Ticker, ESG Score, Carbon Footprint, etc.
        esg_min (int): Minimum acceptable ESG score.
        max_carbon (float): Maximum allowed carbon footprint.
        risk_appetite (str): Risk level - "Low", "Medium", or "High".
        
    Returns:
        cleaned_weights (dict): Optimized weights for each ticker.
        performance (tuple): Portfolio performance metrics (return, volatility, sharpe).
        portfolio_df (pd.DataFrame): DataFrame containing tickers, weights and ESG data.
    """
    price_df = pd.read_csv("data/sample_prices.csv", index_col=0, parse_dates=True)

    print("ESG min:", esg_min)
    print("Max carbon:", max_carbon)

    # Filter assets based on ESG and Carbon Footprint constraints
    filtered = esg_data[(esg_data['ESG Score'] >= esg_min) & (esg_data['Carbon Footprint'] <= max_carbon)]

    print("Filtered assets:")
    print(filtered[['Ticker', 'ESG Score', 'Carbon Footprint']])

    if filtered.empty:
        raise ValueError("No assets match the ESG and Carbon filters. Please loosen your constraints.")

    tickers = filtered['Ticker'].tolist()
    available_tickers = [t for t in tickers if t in price_df.columns]

    if len(available_tickers) < 2:
        raise ValueError("Not enough valid tickers with price data. Please adjust your filters or data.")

    price_data = price_df[available_tickers]

    mu = expected_returns.mean_historical_return(price_data)
    S = risk_models.CovarianceShrinkage(price_data).ledoit_wolf()

    ef = EfficientFrontier(mu, S)

    if risk_appetite == "Low":
        ef.min_volatility()
    elif risk_appetite == "High":
        ef.max_sharpe()
    else:  # Medium risk
        ef.efficient_return(target_return=mu.mean())

    cleaned_weights = ef.clean_weights()
    performance = ef.portfolio_performance(verbose=False)

    portfolio_df = pd.DataFrame({
        "Ticker": list(cleaned_weights.keys()),
        "Weight": list(cleaned_weights.values())
    })

    portfolio_df = portfolio_df[portfolio_df["Weight"] > 0]
    portfolio_df = portfolio_df.merge(esg_data, on="Ticker", how="left")

    return cleaned_weights, performance, portfolio_df
