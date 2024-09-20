import yfinance as yf
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json

# Function to get stock data with retries and store as JSON
def get_stock_data(ticker, start_date, end_date, json_file):
    # Set up retry mechanism
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    
    stock = yf.Ticker(ticker, session=session)
    
    # Fetch historical market data for the stock
    stock_data = stock.history(start=start_date, end=end_date)
    
    # Reset the index to have the date as a column
    stock_data.reset_index(inplace=True)
    
    # Convert DataFrame to JSON format, including date as a key
    stock_data_json = stock_data.to_json(orient="records", date_format="iso")  # records will include date as part of the data
    
    # Save JSON data to a file
    with open(json_file, 'w') as f:
        json.dump(json.loads(stock_data_json), f, indent=4)
    
    print(f"Stock data saved to {json_file}")

# Example usage
ticker_symbol = "INFY"  
start_date = "2023-01-01"
end_date = "2023-09-01"
json_file_path = "stock_data_with_dates.json"  # Path to store the JSON data

# Get stock data and save it to JSON file
get_stock_data(ticker_symbol, start_date, end_date, json_file_path)
