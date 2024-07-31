import os
import sys
sys.path.append(os.getcwd())
from backend import create_app
from wrapper.sharpe import Sharpe
from wrapper.sortino import Sortino

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        s = Sortino()
        print(s.calc_statistics())
    app.run(debug=False)
