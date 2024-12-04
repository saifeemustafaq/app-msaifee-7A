from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    jwt = JWTManager(app)
    db.init_app(app)
    
    # Register blueprints
    from .routes import user_bp, profile_bp, activity_bp, main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(profile_bp, url_prefix='/profiles')
    app.register_blueprint(activity_bp, url_prefix='/activities')
    
    return app 
