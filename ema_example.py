import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

### exponential moving average (EMA)

# S(t) =     Y1  if t=1
#         alpha*Yt + (1- alpha)*St  , t>1

# alpha is degree of decrease
# S(t)  stock prices

## determine trends, identify support levels, resistance levels and directions
## weighted mean of previous S(t)

## function to fetch data from the web Yahoo

def download_data(stock, start_date, end_date):
        ticker = yf.download(stock, start=start_date, end=end_date, progress=False)
        data= pd.DataFrame()

        # Return only the 'Close' column with proper formatting
        data['Price'] = ticker['Close']

        return data

# function to create EMA in given windows
def construct_signals(data, short_period, long_period):
     
     data['Short EMA']= data['Price'].ewm(span= short_period, adjust=False).mean()
     data['Long EMA']= data['Price'].ewm(span= long_period, adjust=False).mean()

     # removing na values
     #data = data.dropna()  # better to drop na in future steps
     #print(data)

## plotting data and EMA
def plot_data(data):
    plt.figure(figsize=(12,6))

    plt.plot( data['Price'], label='Stock Price', color= 'skyblue' )
    plt.plot( data['Short EMA'], label='Short EMA', color= 'red' )
    plt.plot( data['Long EMA'], label='Long EMA', color= 'blue' )
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.title( 'Exponential Moving Average (MA) Indicators')
    plt.show()

if __name__ == '__main__':

    start = "2010-01-05"
    end = "2020-01-05"

    stock_data = download_data('IBM', start, end) 
    
    construct_signals(stock_data, 30,200)

    stock_data = stock_data.dropna()  ## avoid na's in plot

    print(stock_data)

    plot_data(stock_data)
