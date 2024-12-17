from datetime import datetime
import pandas as pd
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv

from Indicators.Volatility.Volumeguage import calculate_indicators

#load environment variables
load_dotenv()

# Credentials for stock data
API_KEY = os.getenv("Alpaca_API")
API_SECRET = os.getenv("Alpaca_Secret")
BASE_URL = "https://paper-api.alpaca.markets"

#Function to save data to a CSV file
def save_to_csv(data, filename):
    """
    Save the given DataFrame to a CSV file.
    :param data: The DataFrame to save.
    :param filename: The name of the CSV file.
    """
    data.to_csv(filename, index=True)
    print(f"Data saved to {filename}")

# Function to fetch stock data
def fetch_stock_data(symbol, timeframe='1Day', start=None, end=None):
    """
    Fetch historical stock data from Alpaca.
    :param symbol: Stock symbol (e.g., 'AAPL')
    :param timeframe: Timeframe for bars ('1Min', '5Min', '1Day', etc.)
    :param start: Start date for data retrieval (e.g., '2023-01-01')
    :param end: End date for data retrieval (e.g., '2023-06-01')
    :return: Pandas DataFrame containing stock OHLCV data
    """
    print(f"Fetching stock data for {symbol}...")
    api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
    if not start:
        start = datetime.now().strftime('%Y-%m-%d')
    if not end:
        end = datetime.now().strftime('%Y-%m-%d')

    bars = api.get_bars(symbol, timeframe, start=start, end=end).df
    return bars[['open', 'high', 'low', 'close', 'volume']]

# Function to fetch crypto data
def fetch_crypto_data(symbol, start, end, timeframe=TimeFrame.Day):
    """
    Fetch historical crypto data from Alpaca.
    :param symbol: Crypto pair (e.g., 'BTC/USD')
    :param start: Start date for data retrieval (datetime object)
    :param end: End date for data retrieval (datetime object)
    :param timeframe: Timeframe for bars (TimeFrame.Day, TimeFrame.Hour, etc.)
    :return: Pandas DataFrame containing crypto OHLCV data
    """
    print(f"Fetching crypto data for {symbol}...")
    client = CryptoHistoricalDataClient()  # No API keys required
    request_params = CryptoBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=timeframe,
        start=start,
        end=end
    )
    bars = client.get_crypto_bars(request_params)
    return bars.df

# Example usage
if __name__ == "__main__":
    # Fetch stock data (e.g., Apple)
    stock_symbol = "AAPL"
    stock_data = fetch_stock_data(stock_symbol, timeframe="1Day", start="2024-06-01", end="2024-06-17")
    save_to_csv(stock_data, f"stock_data_{stock_symbol}.csv")

    # Fetch crypto data (e.g., BTC/USD)
    crypto_symbol = "BTC/USD"
    start_date = datetime(2024, 6, 1)
    end_date = datetime(2024, 6, 7)
    crypto_data = fetch_crypto_data(crypto_symbol, start=start_date, end=end_date)
    save_to_csv(crypto_data, f"crypto_data_{crypto_symbol.replace('/', '_')}.csv")

    #Calculate indicators
    indicators = calculate_indicators(stock_data)
    crypto_indicators = calculate_indicators(crypto_data, atr_length=14)
    print("Calculated Indicators:")
    print(indicators.head())

    #Save indicators to CSV
    indicators_filename = f"calculated_indicators_{stock_symbol}.csv"
    save_to_csv(indicators, indicators_filename)
