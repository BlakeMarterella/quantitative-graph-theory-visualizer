from utils.helper import get_stock_data

def main():
    print("Fetching historical stock data for 'AAPL'...")
    # Get the stock data for 'AAPL' from 2 years ago to today
    aapl_df = get_stock_data('AAPL', start='2021-10-10', end='2021-10-20')
    print("Data fetched successfully!")

if __name__ == "__main__":
    main()