import pandas as pd
import numpy as np
import scipy
from wrapper.metrics import Metrics
from bs4 import BeautifulSoup
import requests
import re

class Sortino(Metrics):
    
    def get_risk_free_rate(self):
        url = "https://www.cnbc.com/quotes/US10Y"
        response = requests.get(url=url)
        
        if response.status_code != 200:
            print(f"Error in getting response: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.content, "html.parser")
        bond_price = soup.find('div', class_="QuoteStrip-lastPriceStripContainer").text
        pattern = r'(\d+\.\d+)%'
        match = re.search(pattern, bond_price)
        
        if match:
            return match.group(1)
        
        print("Bond price could not be found")
        return None
    
    def calc_deviations(self, threshold=0):
        deviations = np.where(self.returns < threshold, self.returns - threshold, 0)
        squared_deviations = deviations ** 2
        mean_squared_deviation = np.mean(squared_deviations)
        return np.sqrt(mean_squared_deviation)
        
        
    def optimize(self):
        num_assets = self.returns.shape[1]
        self.weights = np.array(num_assets * [1. / num_assets])
        
        def sortino(weights):
            risk_free_rate = float(self.get_risk_free_rate()) / 100
            portfolio_return = np.sum(self.returns.mean() * weights) * 252 - risk_free_rate
            downside_deviation = self.calc_deviations()
            portfolio_downside_deviation = np.sqrt(np.dot(weights.T, np.dot(downside_deviation, weights)))
            return -portfolio_return / portfolio_downside_deviation  # Negative because we're minimizing
        
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(num_assets))
        
        optimizer = scipy.optimize.minimize(sortino,
                                            self.weights,
                                            method='SLSQP',
                                            bounds=bounds,
                                            constraints=constraints)
        return optimizer
    
    def calc_statistics(self):
        optimizer = self.optimize()
        self.weights = optimizer.x
        volatility = (self.calc_yearly_volatility() * 100).round(2)
        sharpe_ratio = ((self.calc_yearly_portfolio_returns() / self.calc_yearly_volatility())).round(2)
        return self.weights.round(2), self.calc_yearly_portfolio_returns().round(2), volatility, sharpe_ratio