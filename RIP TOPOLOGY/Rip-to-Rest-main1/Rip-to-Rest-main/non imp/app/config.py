import os
from datetime import timedelta

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///rip_to_rest.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Router configuration
    DEFAULT_ROUTER_PORT = 22  # SSH port
    ROUTER_TIMEOUT = 10  # seconds
    DEFAULT_ROUTER_USERNAME = os.environ.get('DEFAULT_ROUTER_USERNAME')
    DEFAULT_ROUTER_PASSWORD = os.environ.get('DEFAULT_ROUTER_PASSWORD')
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # API configuration
    API_TITLE = 'RIP-to-REST API'
    API_VERSION = '1.0.0'
    API_DESCRIPTION = 'REST API for managing RIP routers'
    
    # Security configuration
    API_KEY_HEADER = 'X-API-Key'
    API_KEY = os.environ.get('API_KEY') or 'dev-api-key'
    
    # CORS configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    RATELIMIT_STORAGE_URL = "memory://"