"""
Initialization of Aegis Scan Backend
"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
jwt = JWTManager()


def create_app():
    """
    Initialization Function
    """
    app = Flask(__name__)
    app.config.from_object('aegis_scan.config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    
    # login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    CORS(app)

    from .routes import core, auth, user

    BLUEPRINTS = [
        core.bp, 
        auth.bp,
        user.bp
    ]

    register_blueprints(app, BLUEPRINTS)

    with app.app_context():
        db.create_all()

    return app


# Register Blueprints Wrapper
def register_blueprints(app, blueprints: list):
    """
    Function to register all provided blueprints
    """
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
