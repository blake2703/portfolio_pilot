import os
import sys
sys.path.append(os.getcwd())
from backend import create_app  # Import create_app
from wrapper.populate_db import fetch_stock_data

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        fetch_stock_data()
    app.run(debug=False)
