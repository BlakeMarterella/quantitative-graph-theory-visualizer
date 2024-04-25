from utils.helper import *

def main():
    portfolio_tickers = []
    # Read all of the stocks in our portfolio
    with open('./portfolio.txt', 'r') as file:
        for line in file:
            portfolio_tickers.append(line.strip())

    # Fetch the historical data for each stock in the portfolio
    portfolio_data = get_portfolio_data(portfolio_tickers)
    
    # Visualize greedy coloring algorithm
    # visualize_greedy_coloring(portfolio_data)
    
    # Visualize Welsh-Powell algorithm
    # visualize_greedy_coloring(portfolio_data)
    
    # Generate Correlation Matrix
    p_correlation_mat = generate_correlation_matrix(portfolio_data)
    
    print(p_correlation_mat)
    

if __name__ == "__main__":
    main()