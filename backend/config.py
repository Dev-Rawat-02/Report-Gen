"""
REPORT-GEN Configuration
Flask application configuration settings
"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # File upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/')
    EXPORT_FOLDER = os.getenv('EXPORT_FOLDER', 'exports/')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB default
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Database settings (if needed)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    
    # API settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    JSONIFY_PRETTYPRINT_REGULAR = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    UPLOAD_FOLDER = 'test_uploads/'
    EXPORT_FOLDER = 'test_exports/'
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    # In production, ensure SECRET_KEY is set via environment variable

# Select configuration based on environment
config_name = os.getenv('FLASK_ENV', 'development')
if config_name == 'testing':
    Config = TestingConfig
elif config_name == 'production':
    Config = ProductionConfig
else:
    Config = DevelopmentConfig