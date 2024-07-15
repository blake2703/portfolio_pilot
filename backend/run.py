import os
import sys
sys.path.append(os.getcwd())
from backend import create_app
from wrapper.populate_db import fetch_stock_data, fetch_stock_prices

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
