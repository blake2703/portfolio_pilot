from abc import abstractmethod, ABC
from database.models import db, Price
import pandas as pd
import numpy as np

class Metrics(ABC):
    
    def __init__(self) -> None:
        self.weights = []
        self.returns = self.calc_yearly_log_returns()
        
    def query_prices_to_df(self):
        # Query all prices from the db table Price
        prices = db.session.query(Price).all()
        
        data = [
            {
                "date": price.date,
                "ticker": price.stock.ticker,
                "open_price": price.open_price,
                "high_price": price.high_price,
                "low_price": price.low_price,
                "close_price": price.close_price,
                "adjusted_close_price": price.adjusted_close_price,
                "volume": price.volume
            }
            for price in prices
        ]
        return pd.DataFrame(data)
        
        
    def calc_yearly_log_returns(self):
        price_data = self.query_prices_to_df()
        price_pivot = price_data.pivot(index='date', columns='ticker', values='adjusted_close_price')
        log_returns = np.log(price_pivot / price_pivot.shift(1))
        return log_returns.dropna()

    def calc_yearly_portfolio_returns(self):
        return np.sum(self.returns.mean() * self.weights) * 252

    def calc_yearly_volatility(self):
        return np.sqrt(np.dot(np.transpose(self.weights), np.dot(self.returns.cov() * 252, self.weights)))
    
    def optimize(self):
        pass
    
    def calc_statistics(self):
        pass
        
    
    
    
    