from flask import Flask, request, jsonify
from flask_cors import CORS
from database.models import db, Stock, Price
import config
import os
import sys
from datetime import datetime

sys.path.append(os.getcwd())

app = Flask(__name__)

@app.before_request 
def before_request(): 
    """
    Allows for webpage to get data returned by flask
    """
    headers = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' } 
    if request.method == 'OPTIONS' or request.method == 'options': 
        return jsonify(headers), 200

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
app.config.from_object(config.DevConfig)
db.init_app(app=app)

# blueprints here
from blueprints.auth import bp as signup_bp
app.register_blueprint(signup_bp)

with app.app_context():
    db.create_all()
    
    # new_stock = Stock(ticker="AAPL", company_name="Apple", sector="Tech", sub_sector="comm")
    # db.session.add(new_stock)
    # db.session.commit()
    
    # price_2023 = Price(stock_id=new_stock.id, date=datetime(2023, 7, 1), open_price=150.0, high_price=155.0, 
    #                    low_price=149.0, close_price=152.0, adjusted_close_price=152.0, volume=1000000)
    # db.session.add(price_2023)
    # db.session.commit()
    
if __name__ == "__main__":
    app.run(debug=False)