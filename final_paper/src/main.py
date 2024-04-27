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
    # apply_extremal_graph_theory(portfolio_data, corr_threshold=0.2, max_clique_size=3, image_name="Extremal_Graph_Theory.png")
    # visualize_welsh_powell_coloring(portfolio_data, threshold=0.2)
    # visualize_greedy_coloring(portfolio_data, threshold=0.2)
    # visualize_graph_with_backtracking(portfolio_data, threshold=0.2)
    
    # Calcualte percent change in entire portfolio
    returns = {name: df['close'].pct_change() for name, df in portfolio_data.items()}
    returns_df = pd.DataFrame(returns)
    # print(returns_df)
    # returns_df['portfolio_return'] = returns_df.sum(axis=1) * 100
    
    # print(portfolio_data["AMD"])
    
    filtered_portfolio = {ticker: data for ticker, data in portfolio_data.items() if ticker in ['AXP', 'BA', 'GS', 'NKE', 'CRM', 'DIS', 'DOW', 'AMD', 'CVX', 'JPM', 'HD', 'INTC', 'MMM', 'MSFT', 'CAT', 'CSCO', 'HON', 'IBM', 'JNJ', 'KO', 'MCD', 'PG', 'TRV', 'UNH', 'VZ', 'V']}
    print("Filtered portfolio:", calculate_roi(filtered_portfolio, initial_investment=300))
    print("Original portfolio:", calculate_roi(portfolio_data, initial_investment=300))
    
    # column_sums = returns_df.sum()
    # sum = 0
    # for returns in column_sums:
    #     sum += returns * 100
    
    # print("Percent change in entire portfolio: ", abs(sum - 3000) / 3000)
    # print(column_sums)

    

if __name__ == "__main__":
    main()