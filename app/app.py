from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize flask_sqlalchemy's SQLalchemy object
db = SQLAlchemy()

# Flask app instance
app = Flask(__name__, template_folder='templates', static_folder='static')

# Login manager instance
login_manager = LoginManager()

# Function to build and make app runable
def create_app():
    # Secret key for hashing sensitive info
    app.secret_key = 'scrypt:32768:8:1$KVIvR0RXMaKYzHq7$5eb7eaf2f52cfcfb99096a1e6c8f436d59b13013933b06aa16cd2f0ba2f336728d32cc7da148adf87156e259efef56951482363a163eeb6d0ad2e988fe9e3fc5'
    # Sqlalchemy databse ref
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_task_db.db'
    
    # Initialize database for this app instance
    db.init_app(app=app)
    
    # Register routes defined in routes.py
    from .routes import register_routes
    register_routes(app=app, db=db)
    
    # Initialize login manager
    login_manager.init_app(app)
    
    
    # Load user model relatively in function to avoid error ( circular import error )
    from .models import User
    
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    # Return flask app for further use ( mostly for launching app )
    return app