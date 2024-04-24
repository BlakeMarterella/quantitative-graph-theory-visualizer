from utils.helper import *

def main():
    portfolio_tickers = []
    # Read all of the stocks in our portfolio
    with open('./portfolio.txt', 'r') as file:
        for line in file:
            portfolio_tickers.append(line.strip())

    # Fetch the historical data for each stock in the portfolio
    portfolio_data = get_portfolio_data(portfolio_tickers)
    
    # Generate Correlation Matrix
    generate_correlation_matrix(portfolio_data)
    

if __name__ == "__main__":
    main()