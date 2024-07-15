import yfinance as yf
from backend import create_app  # Import create_app
from database.models import db, Stock  # Import db and models

SAMPLE_TICKERS = ["AAPL", "TSLA", "SBUX", "HD", "PEP"]

def fetch_stock_data():
    app = create_app()  # Create your Flask app
    with app.app_context():
        for ticker in SAMPLE_TICKERS:
            yf_stock = yf.Ticker(ticker)
            data = yf_stock.info
            stock = Stock.query.filter_by(ticker=ticker).first()
            
            if not stock:
                stock = Stock(
                    ticker=ticker,
                    company_name=data.get('shortName', ''),
                    sector=data.get('sector', ''),
                    sub_sector=data.get('industry', '')
                )
                db.session.add(stock)
                db.session.commit()
                print(f"Added {ticker} to the database.")
            else:
                print(f"Stock {ticker} already exists in the database.")

def fetch_stock_prices():
    """
    Grab last 10 years of stock prices
    """
    

if __name__ == "__main__":
    fetch_stock_data()
