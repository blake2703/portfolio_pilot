from strategy import Strategy
import pandas as pd
import pandas_ta
from utils import preprocess, scrape, get_prices


class Rsi2(Strategy):
    
    def __init__(self, data: pd.DataFrame, prices: pd.DataFrame) -> None:    
        self.data = data
        self.prices = prices
        
        
        self.filter_top_stocks()
        self.feature_engineer()

    
    def filter_top_stocks(self):
        self.data = preprocess(self.data)
        self.data['rsf'] = self.data['rsf'].astype('float')
        self.data['1mo'] = self.data['1mo'].astype('float')
        self.data = self.data[self.data['rsf'] >= 80]
        self.data = self.data.sort_values('1mo', ascending=False)
        self.data = self.data[:25]
    
    def add_ta(self, data):
        """
        This function will calculate the donchian channels based on a 55 day high as well as the rsi 2 for a given 
        stock

        Args:
            data (pd.DataFrame): stock prices data
        """
        data[['donchian_lower', 'donchian_middle', 'donchian_upper']] = pandas_ta.donchian(
            high=data['High'],
            low=data['Low'],
            upper_length=55,
            lower_length=55
        )
        data['rsi2'] = pandas_ta.rsi(
            close=data['Adj Close'],
            length=2
        )
        return data
        
    
    def feature_engineer(self):
        ticker_names = self.data['Symbol'].tolist()
        self.prices = self.prices[self.prices['Ticker'].isin(ticker_names)]
        
        self.prices = self.prices.groupby('Ticker').apply(self.add_ta)
        self.prices['Date'] = pd.to_datetime(self.prices['Date'])
        self.prices = self.prices.dropna()
        
        self.prices['at_donchian_upper'] = self.prices['High'] >= self.prices['donchian_upper']
        self.prices['below_30_rsi2'] = self.prices['rsi2'] <= 30
        self.prices['buy_signal'] = False
        
        self.prices['above_70_rsi2'] = self.prices['rsi2'] >= 70
        self.prices['sell_signal'] = False
        
        
        
    def buy_signal(self):        
        # loop over every ticker
        for ticker in self.prices['Ticker'].unique():
            # get the data for the ticker
            ticker_data = self.prices[self.prices['Ticker'] == ticker]
            # grab index where at donchian upper is true
            donchian_upper_days = ticker_data[ticker_data['at_donchian_upper']].index
            
            # loop over the true values
            for upper_day in donchian_upper_days:
                # Check for subsequent days where rsi2 is below 30
                subsequent_days = ticker_data.loc[upper_day:].index
                
                # loop over subsequent days
                for day in subsequent_days:
                    # if the rsi2 is below 30 of the subsequent day 
                    if ticker_data.loc[day, 'below_30_rsi2']:
                        self.prices.loc[day, 'buy_signal'] = True
                        break  # Exit the loop once a buy signal is found
        

scraped_etfs = pd.read_csv('/Users/blakedickerson/portfolio_pilot/data.csv')
scraped_etf_prices = get_prices(scraped_etfs)

a = Rsi2(data=scraped_etfs, prices=scraped_etf_prices)
a.send_alert()
