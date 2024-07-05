from flask import Blueprint, request, jsonify, make_response
from database.models import db, UserDev
from werkzeug.security import generate_password_hash, check_password_hash
from utils.auth_validator import *

bp = Blueprint("auth", __name__, url_prefix="/auth")

def write_signup_to_db(data):
    """
    Writes a user sign up to the database

    Args:
        data (json): Data returned from the signup form

    Returns:
        bool: Determines if the user was written to the databse successfully
    """
    try:
        password_hash = generate_password_hash(password=data.get('password'))
        
        if not check_password_hash(password_hash, data.get('password')):
            return jsonify({"message": "Password hashing failed"}), 500        

        new_user = UserDev(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password_hash=password_hash
        )
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        return True

    except Exception as e:
        print("Error inserting user into database:", e)
        db.session.rollback()
        return False

@bp.route('/signup', methods=['POST'])
def signup():
    """
    Signs a user up to the service using the /signup endpoint

    Returns:
        json: API response if sign up was successful
    """
    data = request.get_json()
    
    valid_fields, missing_field = validate_signup_fields(data=data)
    if not valid_fields:
        return make_response(jsonify({"message": f"Missing or empty field: {missing_field}"}), 400)
    
    valid_pass = validate_confirm_password(data=data)
    if not valid_pass:
        return make_response(jsonify({"message": "Passwords do not match"}), 400)
    
    valid_signup = write_signup_to_db(data=data)
    if not valid_signup:
        return make_response(jsonify({"message": "Error inserting user into database"}), 500)
    
    return make_response(jsonify({"message": "User signed up successfully"}), 200)