from flask import Flask, request, jsonify
from flask_cors import CORS
from database.models import db
import config

def create_app():
    app = Flask(__name__)
    
    @app.before_request 
    def before_request(): 
        headers = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' } 
        if request.method == 'OPTIONS' or request.method == 'options': 
            return jsonify(headers), 200
    
    cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    app.config.from_object(config.DevConfig)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Register blueprints here
    from blueprints.auth import bp as signup_bp
    app.register_blueprint(signup_bp)
    
    return app
