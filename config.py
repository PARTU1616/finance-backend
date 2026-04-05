import os
from datetime import timedelta

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/finance_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis Session
    SESSION_TYPE = 'redis'
    SESSION_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'finance_session:'
    # Cross-origin cookie settings
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None' if os.environ.get('FLASK_ENV') == 'production' else 'Lax'
    SESSION_COOKIE_DOMAIN = None  # Let browser handle it
    
    # CORS
    CORS_ORIGINS = [origin.strip() for origin in os.environ.get('CORS_ORIGINS', 'http://localhost:9000').split(',')]
