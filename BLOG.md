# Qunatitative Graph Theory Vizualizer

## Getting Started

This tools was created with the intent to help individuals vizualize fluctations in the stock market, the performance of stock holdings overtime, and understand the underlying graph theory driving these changes. With this set of tools, users will be able to view the correlation between stocks and sectors to increase awareness of diversification and experiment with different portfolio allocations. There are additional tools to support future projects in the field of quantitative graph theory by exporting data generated on the site to CSV files.

### Features

- Stock Market Data Exportation Tool

## Software Design and Architecure

I knew that I wanted to use python in some way for this project because of the vast amount of libraries available for data manipulation and graph theory. To that end, I decided to use Flask because of its simplicity. In the future, I would like to implement an API with proper documentation to make the process of integrating datasets into future projects easier. Some of the libraries I am using are:

- Pandas: manipulate the data
- Numpy: to perform calculations
- NetworkX: create the graphs
- Matplotlib: display the graphs.

I also knew that I wanted to use a web framework to create a user interface for the project. I went with VueJS since I had some slight experience in the past. Angular is usually my go-to but I figured it would be too heavy and require more time to set-up. For additional asthetics, I am using TailwindCSS to style the site quickly. With just a few modifications to the `tailwind.config.js` file, I was able to give the site a unique color pallete and implement other uniform style classes throughout the site.

With that, I have a basic understanding of the tools I will be using and how they will interact with each other. I will now begin to set-up the project.

### Repository

I elected to go with a Mono-Repository design for this project. Having both the frontend and backend directory in the same repository will make it easier to manage the project as a whole. At some point, I would like a repository for both the frontend and backend especially if I begin getting support from contributors. For the time being, I will be using the following directory structure:

```
quantitative-graph-theory-visualizer
├── frontend
│   ├── <my vue project>
│
├── backend
│   ├── <my flask project>
│
├── README.md
├── BLOG.md
├── LICENSE
├── .gitignore
├── .gitattributes
├── .editorconfig
├── .env
├── .env.example
├── .git
├── .github
├── .vscode
├── .idea
|_
```

You can view the most up to date version of the project on the [GitHub Repository](https://github.com/BlakeMarterella/quantitative-graph-theory-visualizer)

### Set-Up Frontend

To create a new VueJS project with TailwindCSS, use the Vite to set up a new project. Instructions for how to do this can be found on [Tailwind CSS's official documentation](https://v2.tailwindcss.com/docs/guides/vue-3-vite). Alternatively, you can follow the instructions below:

```shell
# Create a new vite project
npm init vite frontend

# You are now in the directory of your new project!
cd frontend

# Install Vite's front-end dependencies
npm install
```

Next, you will need to install TailwindCSS and its dependencies. You can do this by running the following commands:

```shell
# Install Tailwind and its dependencies
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest

# Create configuration files
npx tailwindcss init -p
```

If you follow the guide above, you will learn more about further optimizations with TailwindCSS. For now, I will be using the default configuration. You can now start the development server with the following command:

```shell
# Start the development server
npm run dev
```

### Set-Up Backend

To create the Flask backend requires a little more manual labor than creating a new frontend project but it's simple with the steps below:

```shell
# Create a new directory for the backend
mkdir backend
cd backend

# Create a new virtual environment
python3 -m venv venv

# Activate the new virtual environment (you will need to do this anytime you close your terminal)
source venv/bin/activate

# Install Flask
pip install Flask
```

Now you will need to create the entry point to your flask app:

```shell
# Create a new file called app.py
touch app.py
```

My project all started with this sample code:

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

## The First Feature

The first feature that I am going to implement is the Stock Market Data Exportation Tool. This tool will allow users to input a stock symbol and a date range and receive a CSV file with the stock data for that date range. This will be useful for users who want to analyze the data in a spreadsheet or use it in another program. Additionally, I chose it as my first feature becasuse I will use it to perform calculations for my paper with the various data sets that my site generate.

### Selecting a Historical Stock API

There are many historical stock API's that I can choose from but a lot of them are either too expensive or have limitations on the number of requests that can be made. Some of the APIs, such as [Alpaca API](https://alpaca.markets/) which I have experience with in the past supports real-time data and trading which is a little more than is needed at this time. I elected to go with the [Alpha Advantage](https://www.alphavantage.co/) API because of it's realtime and historical stock market data, the ability to support analysis of different commodoties such as cryptocurrency, forex, etc. (this may be important for future development), and the fact that it is free to use (for up to 25 requests per day). The processes for generating a token was as easy as entering in my university email.

*Update*: The 25 requests per day were not enough so I decided to purchase the premium version of the API. This will allow me to make up to 75 requests per minute which should be more than enough for the purposes of this project.

### Implementing the API

After recieving the API key, I created a `.env` file in the root of my project and adding the key (see `example.env` for formatting). This ensures that my API key is not exposed to the public. After this initial configuration, we will be able to use any Alpha endpoint safe and securely without any worry. This endpoint and future API endpoints will follow these steps (or a similar process):

1. Create a new route in Flask
2. Query the Alpha Advantage API
3. Process Data
4. Return Data

For the purpose of the demonstration, I will describe how I performed each one of these steps below for my new endpoint `historical-stock-data`.

#### __Step 1__: Create new route in Flask

This step may be the easiest step, all that is needed is the decorator to specify the route and a new function:
```python
@app.route('/historical_data/<ticker>')
def get_ticker(ticker):
    return "HELLO WORLD!"
```

#### __Step 2__: Query the Alpha Advantage API

I will be using the `requests` library so that my Flask API can make requests to the Alpha Advantage. The Alpha endpoint I am using is [`TIME_SERIES_DAILY`](https://www.alphavantage.co/documentation/#daily) because it has 20+ years of historical data for any given stock ticker. If you look at the official documentation you can see the various parameters that can be passed to the endpoint.

```python
    # Retrieve parameters from the query string
    symbol = request.args.get('symbol', default='IBM', type=str)  # Default to 'IBM' if not provided
    outputsize = request.args.get('outputsize', default='full', type=str)  # Default to 'compact'
    datatype = request.args.get('datatype', default='json', type=str)  # Default to 'json', 'csv' is also supported

    # Construct the API URL
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize={outputsize}&datatype={datatype}&apikey={API_KEY}"

    # Make the GET request
    response = requests.get(url)
```

#### __Step 3__: Process Data

Now that the response has been recieved from the API, it's time to process the data. Since the API does not allow me to specify a date range, I will have to filter the data on my end using pandas.

```python
# First check if the request was successful
response.status_code == 200:
        if datatype == 'json':
            data = response.json()
            df = pd.DataFrame(data['Time Series (Daily)']).T
            df.index = pd.to_datetime(df.index)
            # Filter data based on date range
            if start_date and end_date:
                df = df[start_date:end_date]

            # Convert DataFrame back to JSON
            result = df.to_json()
            return result
        elif datatype == 'csv':
            # Read CSV into DataFrame
            from io import StringIO
            df = pd.read_csv(StringIO(response.text), index_col=0)
            df.index = pd.to_datetime(df.index)
            if start_date and end_date:
                df = df[start_date:end_date]
```

### Testing the endpoint

To test the endpoint, I am using Postman. Postman is a great tool for testing APIs because it allows you to make requests to your API and see the response. It also allows you to set up tests to ensure that your API is working correctly. I will be using Postman to test the `historical-stock-data` endpoint that I just created.

In the screenshot below, you can see that I request historical data for `AMD` stock for January 2024. The response is a JSON object with the stock data for that date range.



### Implement Frontend


## Refactoring API with Swagger

Everything up to this point has been simple, straightforward, and perfect for building a quick API for a personal project. However, as the project grows, it will be important to have proper documentation for the API. This is where Swagger comes in. Swagger is a tool that allows you to create interactive documentation for your API. It is a great way to keep track of all the endpoints, parameters, and responses that your API supports. It also allows you to test your API directly from the documentation page (something that I could've used when I was building the first feature).
