import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

## function to fetch data from the web Yahoo

def download_data(stock, start_date, end_date):
        ticker = yf.download(stock, start=start_date, end=end_date, progress=False)
        data= pd.DataFrame()

        # Return only the 'Close' column with proper formatting
        data['Price'] = ticker['Close']

        return data

# function to create SMA in given windows
def construct_signals(data, short_period, long_period):
     
     data['Short SMA']= data['Price'].rolling(window=short_period).mean()
     data['Long SMA']= data['Price'].rolling(window=long_period).mean()

     # removing na values
     #data = data.dropna()  # better to drop na in future steps
     #print(data)

## plotting data and SMA
def plot_data(data):
    plt.figure(figsize=(12,6))

    plt.plot( data['Price'], label='Stock Price', color= 'black' )
    plt.plot( data['Short SMA'], label='Short SMA', color= 'red' )
    plt.plot( data['Long SMA'], label='Long SMA', color= 'blue' )
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.title( 'Moving Average (MA) Indicators')
    plt.show()

if __name__ == '__main__':

    start = "2010-01-05"
    end = "2020-01-05"

    stock_data = download_data('IBM', start, end) 
    
    construct_signals(stock_data, 30,200)

    stock_data = stock_data.dropna()  ## avoid na's in plot

    print(stock_data)

    plot_data(stock_data)