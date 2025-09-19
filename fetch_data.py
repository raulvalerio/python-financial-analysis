## install ?
#  pip install yfinance

import yfinance as yf
import pandas as pd

## function to fetch data from the web Yahoo

def download_data_secure(stock, start_date, end_date):
    try:
        # Download historical data
        ticker = yf.download(stock, start=start_date, end=end_date, progress=False)

 #       # Check if data is valid
        if ticker.empty or 'Close' not in ticker.columns:
           print(f"No valid data found for {stock}.")
           return pd.DataFrame()

        # Return only the 'Close' column with proper formatting
        return ticker[['Close']].rename(columns={'Close': 'price'})

    except Exception as e:
        print(f"Error downloading data: {e}")
        return pd.DataFrame()

def download_data(stock, start_date, end_date):
        ticker = yf.download(stock, start=start_date, end=end_date, progress=False)
        data= pd.DataFrame()

        # Return only the 'Close' column with proper formatting
        data['Price'] = ticker['Close']

        return data

if __name__ == '__main__':
    start = "2010-01-05"
    end = "2015-01-05"

    stock_data = download_data('IBM', start, end) 
    print(stock_data.head())
