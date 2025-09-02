"""
Base database configuration and setup
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Initialize SQLAlchemy
db = SQLAlchemy()
Base = declarative_base()

# Database configuration
DATABASE_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5433'),
    'database': os.environ.get('DB_NAME', 'landscaper'),
    'username': os.environ.get('DB_USER', 'landscaper_user'),
    'password': os.environ.get('DB_PASSWORD', 'landscaper_password_2024')
}

def get_database_url():
    """Get database URL from environment or use defaults"""
    return f"postgresql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

def init_database(app):
    """Initialize database with Flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {'connect_timeout': 10}
    }
    
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
    
    return db
