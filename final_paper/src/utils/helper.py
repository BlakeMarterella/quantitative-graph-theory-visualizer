import requests
import csv
from datetime import datetime, timedelta
import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt
import json

BASE_URL = "http://127.0.0.1:5000/"

def generate_correlation_matrix(portfolio_data):
    """
    
    """
    '''         Step 1: Data Preparation      '''
    returns = {name: df['close'].pct_change() for name, df in portfolio_data.items()}
    returns_df = pd.DataFrame(returns)

    # Compute correlation matrix
    correlation_matrix = returns_df.corr()

    '''         Step 2: Graph Construction      '''
    
    threshold = 0.5  # Define your own threshold
    G = nx.Graph()
    for stock1 in correlation_matrix.columns:
        for stock2 in correlation_matrix.index:
            if stock1 != stock2 and correlation_matrix.loc[stock1, stock2] > threshold:
                G.add_edge(stock1, stock2, weight=correlation_matrix.loc[stock1, stock2])


    '''         STEP 3: Applying Extremal Graph Theory          '''
    # Analyze Graph Properties: Investigate properties like maximum degree, diameter, or other relevant metrics that can be derived from extremal graph theory.
    print(correlation_matrix)
    degree_sequence = dict(G.degree()).values()

    if degree_sequence:
        max_degree = max(degree_sequence)
    else:
        print('No edges found in the graph')
        
    # max_degree = max(dict(G.degree()).values())
    diameter = nx.diameter(G)
    # Add more analyses as needed


    '''         Step 4: Visualization       '''
    import matplotlib.pyplot as plt
    # Use your graph G from previous steps
    pos = nx.spring_layout(G)  # Positions for all nodes

    # Draw the graph (nodes and edges)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, 
            edge_color='gray', linewidths=0.5,
            font_size=10)

    # Prepare edge labels, truncated to 4 decimal places
    edge_labels = {(u, v): f"{d['weight']:.4f}" for u, v, d in G.edges(data=True)}

    # Draw edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.axis('off')  # Turn off the axis
    plt.show()  # Display the graph
    

def get_portfolio_data(tickers):
    """
    Fetch the historical data for a list of stock tickers that are in a portfolio.
    - 4 years of historical data for a stock will be provided.
    - If the data for any stock has been fetched previously, it will be loaded from the CSV file.
    
    Parameters:
    tickers (list): A list of stock tickers.
    
    Returns:
    dict: A dictionary containing the stock data for each ticker.
    """
    portfolio_data = {}
    
    for ticker in tickers:
        # Get the stock data for each ticker from 2 years ago to today
        ticker_df = get_stock_data(ticker)

        if ticker_df.empty:
            print(f"Failed to fetch data for {ticker}!")
            break
        else:
            portfolio_data[ticker] = ticker_df
        
    return portfolio_data
            


def get_stock_data(ticker, start=None, end=None):
    """
    Fetches historical stock data for a given ticker symbol within a specified date range.
    
    By default this function will return a dataframe with
    data from the last 4 years to the current data.
    
    Parameters:
    ticker (str): The ticker symbol of the stock.
    start (str, optional): The start date in the format 'YYYY-MM-DD'. Defaults to 2 years ago from today.
    end (str, optional): The end date in the format 'YYYY-MM-DD'. Defaults to today.
    
    Returns:
    DataFrame: A pandas DataFrame containing the historical stock data.
    """
    # Input Validation
    if start is None:
        start = (datetime.now() - timedelta(days=365*4)).strftime('%Y-%m-%d')
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

            df['date'] = pd.to_datetime(df['date'])
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(path), exist_ok=True)

            # Save the DataFrame to a CSV file
            df.to_csv(path, index=False)

            return df

        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return None
        
    # Data has been fetched previously, so load the CSV file
    else:
        df = pd.read_csv(path)
        # print("Data loaded from CSV file.")
        return df
