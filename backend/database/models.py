from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class UserDev(db.Model):
    # Define table name
    __tablename__ = "users_dev"
    
    # Define schema
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    
    @property
    def password(self):
        """
        Determines if the password is hashable
        """
        raise AttributeError("Password is not hashable")
    
    @password.setter
    def password(self, password):
        """
        Helper function to generate password before it reaches the database

        Args:
            password (str): Password inputted by user
        """
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """
        Verifies if the hashed password is equivalent to the non-hashed password

        Args:
            password (str): Password inputted by user

        Returns:
            bool: Determines if the passwords are equivalent
        """
        return check_password_hash(self.password_hash, password)
    
    