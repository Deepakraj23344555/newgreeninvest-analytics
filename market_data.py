import yfinance as yf

def get_live_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.info['currentPrice']
