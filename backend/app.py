from flask import Flask, jsonify
import os
from dotenv import load_dotenv

# Load environment variable from the .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return API_KEY

if __name__ == '__main__':
    app.run(debug=True)