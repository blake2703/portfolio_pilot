import os
import sys
sys.path.append(os.getcwd())
from backend import create_app
from wrapper.metrics import get_returns, calc_statistics_sharpe
import numpy as np

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        rets = get_returns()
        print(calc_statistics_sharpe(rets))
    app.run(debug=False)
