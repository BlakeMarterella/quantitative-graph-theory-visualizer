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

There are many historical stock API's that I can choose from but a lot of them are either too expensive or have limitations on the number of requests that can be made. Some of the APIs, such as [Alpaca API](https://alpaca.markets/) which I have experience with in the past supports real-time data and trading which is a little more than is needed at this time. I elected to go with the [Alpha Advantage](https://www.alphavantage.co/) API because of it's realtime and historical stock market data, the ability to support analysis of different commodoties such as cryptocurrency, forex, etc. (this may be important for future development), and the fact that it is free to use. The processes for generating a token was as easy as entering in my university email.

### Implementing the API

After recieving the API key, I created a `.env` file in the root of my project and adding the key (see `example.env` for formatting). This ensures that my API key is not exposed to the public.

The Alpha endpoint I am using is [`TIME_SERIES_INTRADAY`](https://www.alphavantage.co/documentation/) because it has 20+ years of historical data for any given stock ticker.

I will be using the `requests` library so that my Flask API can make requests to the Alpha Advantage API. The first endpoint that I will be using will not require any processing on the data so it will be a simple GET request to the Alpha API and my Flask API returning the result. I chose the endpoint `historical_data/<ticker>`. You can view the code in `app.py` for a more extensive look on how the `GET` request is implemented in Flask.