import pandas as pd
import numpy as np
import scipy
from wrapper.metrics import Metrics

import scipy.optimize

class Sharpe(Metrics):

    def optimize(self):
        num_assets = self.returns.shape[1]
        self.weights = np.array(num_assets * [1. / num_assets])

        def sharpe_neg(weights):
            self.weights = weights
            yearly_volatility = self.calc_yearly_volatility()
            portfolio_return = self.calc_yearly_portfolio_returns()
            if yearly_volatility == 0:
                return np.inf  # Avoid division by zero
            return -portfolio_return / yearly_volatility

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(num_assets))

        optimizer = scipy.optimize.minimize(sharpe_neg,
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
