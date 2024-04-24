import requests
import csv
from datetime import datetime, timedelta
import pandas as pd
import os
import json

BASE_URL = "http://127.0.0.1:5000/"

def get_stock_data(ticker, start=None, end=None):
    """
    Fetches historical stock data for a given ticker symbol within a specified date range.
    
    Parameters:
    ticker (str): The ticker symbol of the stock.
    start (str, optional): The start date in the format 'YYYY-MM-DD'. Defaults to 2 years ago from today.
    end (str, optional): The end date in the format 'YYYY-MM-DD'. Defaults to today.
    
    Returns:
    DataFrame: A pandas DataFrame containing the historical stock data.
    """
    # Input Validation
    if start is None:
        start = (datetime.now() - timedelta(days=365*2)).strftime('%Y-%m-%d')
    if end is None:
        end = datetime.now().strftime('%Y-%m-%d')
    
    # Generate a unique filename for the CSV file
    filename = f"{ticker}_{start}_{end}.csv"
    path = f"./datasets/{filename}"
    
    # To reduce redundant API calls, only fetch data if the CSV file does not exist
    if not (os.path.exists(path)):
        # Define the URL and the query parameters
        url = f"{BASE_URL}historical-stock-data"
        params = {
            "symbol": ticker,  # Make sure 'ticker', 'start', and 'end' are defined or passed to this script
            "start": start,
            "end": end,
            "datatype": "json"
        }

        # Make the GET request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Load the JSON data into a Pandas DataFrame
            data = response.json()  # Assume the JSON structure matches what pandas expects
            json_data = json.loads(data['data'])
            
            df = pd.DataFrame(json_data) 
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(path), exist_ok=True)

            # Save the DataFrame to a CSV file
            df.to_csv(path, index=False)

            # Optional: Display the DataFrame or perform additional data processing
            print(df.head())

            return df

        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return None
        
    # Data has been fetched previously, so load the CSV file
    else:
        df = pd.read_csv(path)
        print("Data loaded from CSV file.")
        return df
