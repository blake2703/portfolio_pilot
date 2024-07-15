import yfinance as yf
from database.models import db, Stock, Price
import pandas as pd
from sqlalchemy import distinct, func
import numpy as np
import scipy
from typing import List

def query_prices_to_df():
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

def get_returns():
    """
    Calculate the log returns of a portfolio

    Returns:
        pd.Dataframe: df containing log returns of each individual ticker
    """
    price_data = query_prices_to_df()
    price_pivot = price_data.pivot(index='date', columns='ticker', values='adjusted_close_price')
    log_returns = np.log(price_pivot / price_pivot.shift(1))
    return log_returns.dropna()


def calc_yearly_portfolio_returns(returns: pd.DataFrame,
                                  weights: List[float]):
    """
    Take the average value of the returns df and multiply by the weighting of each stock in the portfolio. We assume
    there are 252 trading days a year, so we multiply this to the end
    
    Returns:
        float: yearly returns of a portfolio
    """
    return np.sum(returns.mean() * weights) * 252

def calc_yearly_volatility(returns: pd.DataFrame,
                           weights: List[float]):
    """
    Calculate the yearly volatility of a portfolio

    Args:
        returns (pd.DataFrame): df containing log returns of each individual ticker
        weights (List[int]): weights for individual tickers in a portfolio

    Returns:
        float: yearly volatility of a portfolio
    """
    return np.sqrt(np.dot(np.transpose(weights), np.dot(returns.cov() * 252, weights)))

def optimize_portfolio_sharpe(returns: pd.DataFrame):
    """
    Builds an optimizer to optimize the weights of a portfolio using the Sharpe Ratio

    Args:
        returns (pd.Dataframe): df containing log returns of each individual ticker

    Returns:
        scipy.optimizer: an optimizer model
    """
    num_assets = returns.shape[1]
    weights = np.array(num_assets * [1. / num_assets,])
    
    def sharpe_neg(weights: List[float]):
        """
        Calculates the negative sharpe ratio with equal weights for each individual ticker

        Args:
            weights (List[int]): weights for individual tickers in a portfolio

        Returns:
            float: negative sharpe value to be optimized
        """
        portfolio_return = calc_yearly_portfolio_returns(returns, weights)
        portfolio_volatility = calc_yearly_volatility(returns, weights)
        return -portfolio_return / portfolio_volatility
    
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    
    optimizer = scipy.optimize.minimize(sharpe_neg,
                                        weights,
                                        method='SLSQP',
                                        bounds=bounds,
                                        constraints=constraints)
    
    return optimizer 

def calc_statistics_sharpe(returns: pd.DataFrame):
    """
    Calculates the statistics of the optimizer

    Args:
        returns (pd.DataFrame): weights for individual tickers in a portfolio

    Returns:
        List[float]: optimal weights for a portfolio
        float: yearly return of a portfolio with optimal weights
        float: yearly volatility of a portfolio with optimal weights
        float: sharpe ratio with optimal weights
    """
    optimizer = optimize_portfolio_sharpe(returns=returns)
    optimal_weight_percentage = (optimizer['x'] * 100).round(2)
    portfolio_return = (calc_yearly_portfolio_returns(returns=returns, weights=optimizer['x']) * 100).round(2)
    volatility = (calc_yearly_volatility(returns=returns, weights=optimizer['x']) * 100).round(2)
    sharpe_ratio = (calc_yearly_portfolio_returns(returns=returns, weights=optimizer['x']) / calc_yearly_volatility(returns=returns, weights=optimizer['x'])).round(2)
    return optimal_weight_percentage, portfolio_return, volatility, sharpe_ratio
    
    
    
