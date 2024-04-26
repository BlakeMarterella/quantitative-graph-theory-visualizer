from utils.helper import *

def main():
    portfolio_tickers = []
    # Read all of the stocks in our portfolio
    with open('./portfolio.txt', 'r') as file:
        for line in file:
            portfolio_tickers.append(line.strip())

    # Fetch the historical data for each stock in the portfolio
    portfolio_data = get_portfolio_data(portfolio_tickers)
    
    # generate_correlation_graph(portfolio_data)
    apply_extremal_graph_theory(portfolio_data, corr_threshold=0.2, max_clique_size=3, image_name="Extremal_Graph_Theory.png")
    

if __name__ == "__main__":
    main()