import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime

class MovingAverageCrossover:

    def __init__(self, capital, stock, start, end, short_period,long_period):
        self.data= None
        self.is_long= False
        self.short_period = short_period
        self.long_period = long_period
        self.capital = capital         ## inital budget
        self.equity = [capital ] # what is the profit making?, equitiy curve
        self.stock = stock  ## company
        self.start = start
        self.end = end
    
    def download_data(self):
        stock_data = pd.DataFrame()
        ticker = yf.download(self.stock, self.start, self.end,progress=False)
        stock_data['Price']= ticker['Close']
        self.data = stock_data
    
    def simulate(self):
        ## we consider all the trading days and decide whether to open a
        ## long positon or not
        
        price_when_buy=0

        for index, row in self.data.iterrows():      ### iterate through rows

            ## CLOSE THE LONG POSITION WE HAVE OPENED
            if row.short_ma < row.long_ma and self.is_long :      ## same notation   row.short_ma -> row['short_ma']
                self.equity.append(self.capital * row.Price / price_when_buy)
                self.is_long = False
                #print(" -- SELL -- : " , index)
            elif row['short_ma'] > row['long_ma'] and not self.is_long:
                ## OPEN A LONG POSITION
                price_when_buy = row['Price']
                self.is_long =True
                #print(" -- BUY -- ", index)
        
    def plot_equity(self):

        print("Profit of the trading strategy: %.2f%%" % ( 
           (float(self.equity[-1]) -  float(self.equity[0])) /
           float(self.equity[0])*100
           ) 
        )

        print("Actual capital: $%0.2f" %self.equity[-1])

        plt.figure(figsize= (12,6))
        plt.plot(self.equity, label = "Stock Price", color="green")
        plt.xlabel('Date')
        plt.ylabel("Actual Capital ($)")
        plt.title("Equity Curve for CrossOver strategy at " + self.stock)
        plt.show()

    ## exponential moving average
    def construct_signals(self):
        self.data['short_ma']= self.data['Price'].ewm(span=self.short_period).mean()
        self.data['long_ma']= self.data['Price'].ewm(span=self.long_period).mean()

    def plot_signals(self):
        plt.figure(figsize=(12,6))
        plt.plot(self.data['Price'], label="Stock Price", color='black')
        plt.plot(self.data.short_ma, label="Short MA", color='blue')
        plt.plot(self.data.long_ma, label="Long MA", color='green')
        plt.title("Moving Average (MA) Crossover Trading Strategy for " + self.stock)
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.legend(loc="upper left")
        plt.show()


if __name__ == '__main__':
    start_date = datetime.datetime(2010,1,1)
    end_date = datetime.datetime(2020,7,1)

    strategy = MovingAverageCrossover(100, 'MSFT',start_date, end_date, 30,100)
    strategy.download_data()
    strategy.construct_signals()
    strategy.plot_signals()
    strategy.simulate()
    print(" Equity: ", strategy.equity)

    strategy.plot_equity()

    #print(strategy.data)
