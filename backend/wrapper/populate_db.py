import yfinance as yf
from database.models import db, Stock, Price
from datetime import datetime

SAMPLE_TICKERS = ["AAPL", "TSLA", "SBUX", "HD", "PEP"]

def fetch_stock_data():
    """
    Add sample stocks to stocks table
    """
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
    Grab 10 years of stock prices and populate the price table.
    """
    for ticker in SAMPLE_TICKERS:
        stock = Stock.query.filter_by(ticker=ticker).first()
        if stock:
            prices = yf.download(tickers=ticker, start=datetime(2010, 1, 1), end=datetime(2020, 1, 1))
            for date, row in prices.iterrows():
                existing_price = Price.query.filter_by(stock_id=stock.id, date=date).first()
                if not existing_price:
                    price = Price(
                        stock_id=stock.id,
                        date=date,
                        open_price=row['Open'],
                        high_price=row['High'],
                        low_price=row['Low'],
                        close_price=row['Close'],
                        adjusted_close_price=row['Adj Close'],
                        volume=row['Volume']
                    )
                    db.session.add(price)
                    db.session.commit()
        else:
            print(f"Stock {ticker} does not exist in the database.")
            
    
    

if __name__ == "__main__":
    fetch_stock_data()
    fetch_stock_prices()
