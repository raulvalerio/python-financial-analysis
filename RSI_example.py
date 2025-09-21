## Relative strength Indicator  ( 1 - 100)
##RSI =  100 - [ (100)/ ( 1 +  avg_gain / avg_loss   )]

## standard days is 14 for the period

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

def download_data(stock, start, end):
    data= pd.DataFrame()
    ticker = yf.download(stock, start, end)
    data['Price'] = ticker['Close']
    
    return data

if __name__ == '__main__':

    startdate = datetime.datetime(2015,1,1)
    enddate = datetime.datetime(2020,1,1)

    stockdata = download_data('IBM', startdate, enddate)
    
    stockdata['return'] = np.log(  stockdata['Price'] / stockdata['Price'].shift(1))   ### moving to the right and calculate ratio   today value / yesterday value
                                                    ## return is a profit on a given investment
    stockdata['move'] = stockdata['Price'] - stockdata['Price'].shift(1)       ## substracting

    stockdata['up'] = np.where(stockdata['move']>0, stockdata['move'],0)   ### if else
    stockdata['down'] = np.where(stockdata['move']<0, stockdata['move'],0)

    #RSI  
    ## window = 14  period
    stockdata['average_gain'] = stockdata['up'].rolling(14).mean()
    stockdata['average_loss'] = stockdata['down'].abs().rolling(14).mean()  ## must be positive -> use abs

    RS = stockdata['average_gain'] / stockdata['average_loss']

    stockdata['rsi'] = 100.0 - ( 100.0/(1.0 + RS) )

    stockdata= stockdata.dropna()

    #print( stockdata)
    plt.plot( stockdata['rsi'])
    plt.show()