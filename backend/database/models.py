from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, text, event

db = SQLAlchemy()

class UserDev(db.Model):
    # Define table name
    __tablename__ = "users_dev"
    
    # Define schema
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    
    @property
    def password(self):
        raise AttributeError("Password is not readable")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Stock(db.Model):
    __tablename__ = "stocks"
    
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    company_name = db.Column(db.String(128), nullable=False)
    sector = db.Column(db.String(128), nullable=False)
    sub_sector = db.Column(db.String(128), nullable=False)
    
    prices = relationship("Price", back_populates="stock")

class Price(db.Model):
    """
    Creates a table to hold stock prices. It will reference the stocks table in order to assign an
    ID 

    Args:
        db (_type_): _description_
    """
    __tablename__ = "prices"
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    stock_id = db.Column(db.Integer, ForeignKey("stocks.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    adjusted_close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    
    stock = relationship("Stock", back_populates="prices")