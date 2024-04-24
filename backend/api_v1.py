from flask import Flask, jsonify, request, make_response
import os
import requests
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS
import pandas as pd
from datetime import datetime

# Load environment variable from the .env file (if it exists)
_env_file = find_dotenv()
if _env_file:
    load_dotenv(_env_file)
    
API_KEY = os.getenv('ALPHA_API_KEY')

# Create a new app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, automatic_options=True)

"""
Proof of concept first route to test the Flask app
"""
@app.route('/')
def hello_world():
    return "Hello World!"

"""
This route will return the historical stock data 
for a given ticker symbol.

Route: /historical-stock-data
Request Type: GET
Parameters:
    - symbol: The ticker symbol of the stock (required)
    - outputsize: The size of the output data (optional, default='full') 
        options: ['full', 'compact']
    - outputtype: The type of output data (optional, default='json')
        options: ['json', 'csv']
    - start: The start date of the data (optional)
    - end: The end date of the data (optional)
        If end date is not specified, it will default to the current date
"""
@app.route('/historical-stock-data', methods=['GET', 'OPTIONS'])
def historical_stock_data():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    symbol = request.args.get('symbol', type=str)
    outputsize = request.args.get('outputsize', default='full', type=str)  # Optional
    outputtype = request.args.get('outputtype', default='json', type=str) # Optional
    start_date = request.args.get('start', default=None) # Optional
    end_date = request.args.get('end', default=None) # Optional
    
    # Verify that the symbol is not empty
    if not symbol:
        return jsonify({"error": "Symbol is required"}), 400
    
    # Convert start_date and end_date to datetime objects if they are provided
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    if start_date and end_date:
        # Validate the date range
        if start_date > end_date:
            return jsonify({"error": "Start date must be before end date"}), 400
        
    if start_date:
        # Verify that the start date is greater than January 1, 2000
        if start_date < datetime.strptime('2000-01-01', '%Y-%m-%d'):
            return jsonify({"error": "Start date must be greater than January 1, 2000"}), 400
        # If end date is not specified, set it to the current date
        if not end_date:
            end_date = datetime.today()
    
    if end_date:
        # Verify that the end date is less than the current date
        if end_date > datetime.today():
            return jsonify({"error": "End date must be less than the current date"}), 400

    # Verify that the outputtype is either 'json' or 'csv'
    if outputtype not in ['json', 'csv']:
        return jsonify({"error": "Output type must be 'json' or 'csv'"}), 400

    # Construct the API URL
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize={outputsize}&datetype=json&apikey={API_KEY}"
    # The response will always be JSON and the conversion will happen later in this funciton

    # Make the GET request
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['Time Series (Daily)']).T
        df.index = pd.to_datetime(df.index)
        
        # Rename the columns
        df['date'] = df.index
        df = df.rename(columns={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
        
        
        # Reorder the columns with the date first
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        
        # Filter data based on date range
        if start_date and end_date:
            df = df.loc[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        # Remove the index column
        df = df.dropna().reset_index().drop(columns = 'index')
            
        if outputtype == 'json':
            result = df.to_json()
            return jsonify({"data": result}), 200, {'Content-Type': 'application/json'}
        elif outputtype == 'csv':
            # Convert DataFrame back to CSV
            return df.to_csv(), 200, {'Content-Type': 'text/csv'}
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)