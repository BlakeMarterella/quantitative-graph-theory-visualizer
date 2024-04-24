from utils.helper import get_stock_data, get_portfolio_data

def main():
    portfolio_tickers = []
    # Read all of the stocks in our portfolio
    with open('./portfolio.txt', 'r') as file:
        for line in file:
            portfolio_tickers.append(line.strip())

    # Fetch the historical data for each stock in the portfolio
    portfolio_data = get_portfolio_data(portfolio_tickers)
            

    # print("All data fetched!")

if __name__ == "__main__":
    main()