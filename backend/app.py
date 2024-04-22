from flask import Flask, jsonify
import os
import requests
from dotenv import load_dotenv

# Load environment variable from the .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return API_KEY

@app.route('/ticker/<ticker>')
def get_ticker(ticker):
    # Construct the URL with the passed ticker symbol and the API key
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={API_KEY}'

    # Make the GET request to Alpha Vantage API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON response from Alpha Vantage
        return jsonify(response.json())
    else:
        # Return an error if something went wrong
        return jsonify({"error": "Failed to fetch data"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)