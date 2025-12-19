"""
Application configuration for different environments.

Configurations are loaded based on the FLASK_ENV environment variable.
"""

import os
from datetime import timedelta


class BaseConfig:
    """Base configuration with common settings."""

    # Application
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_REFRESH_EACH_REQUEST = True

    # Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_SECURE = False  # Set to True in production
    REMEMBER_COOKIE_HTTPONLY = True

    # WTForms
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # CSRF tokens don't expire

    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'memory://'
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_HEADERS_ENABLED = True

    # Caching
    CACHE_TYPE = 'SimpleCache'  # Will be Redis in production
    CACHE_DEFAULT_TIMEOUT = 300

    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = None
    LOG_MAX_BYTES = 10485760  # 10MB
    LOG_BACKUP_COUNT = 10

    # Email (for password reset, email verification)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@quiz-app.local'

    # Sentry (Error Tracking)
    SENTRY_DSN = os.environ.get('SENTRY_DSN')

    # Quiz Settings
    QUESTIONS_PER_PAGE = 1  # One question at a time
    QUIZ_SESSION_TIMEOUT = timedelta(hours=2)  # Auto-expire quiz sessions

    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
    }


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""

    DEBUG = True
    TESTING = False

    # Database - SQLite for development (fallback to PostgreSQL if DATABASE_URL is set)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dev_quiz_app.db')

    SQLALCHEMY_ECHO = False  # Set to True to see SQL queries

    # Disable CSRF for easier development (enable in testing/production)
    WTF_CSRF_ENABLED = True  # Keep enabled even in dev for consistency

    # Session cookies (not secure over HTTP in dev)
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

    # Logging
    LOG_LEVEL = 'DEBUG'

    # Cache - Simple in-memory cache for development
    CACHE_TYPE = 'SimpleCache'


class TestingConfig(BaseConfig):
    """Testing environment configuration."""

    DEBUG = False
    TESTING = True

    # Database - Separate test database
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_quiz_app.db')

    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False

    # Disable rate limiting for tests
    RATELIMIT_ENABLED = False

    # Use simple cache for tests
    CACHE_TYPE = 'SimpleCache'

    # Shorter session lifetime for tests
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)

    # Logging
    LOG_LEVEL = 'ERROR'  # Only log errors during tests


class StagingConfig(BaseConfig):
    """Staging environment configuration (pre-production testing)."""

    DEBUG = False
    TESTING = False

    # Database - PostgreSQL required
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://quiz_user:quiz_pass@localhost/quiz_app_staging'

    # Redis for caching and rate limiting
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'

    # Session - Redis backed
    SESSION_TYPE = 'redis'
    SESSION_REDIS = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'

    # Security (HTTPS recommended but not required in staging)
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = '/var/log/quiz-app/staging.log'


class ProductionConfig(BaseConfig):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False

    # Database - PostgreSQL required (will be validated when config is actually used)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or None

    # Redis for caching and rate limiting (required)
    REDIS_URL = os.environ.get('REDIS_URL') or None

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = REDIS_URL
    RATELIMIT_STORAGE_URL = REDIS_URL

    # Session - Redis backed (required for production)
    SESSION_TYPE = 'redis'
    SESSION_REDIS = REDIS_URL

    # Security (HTTPS required)
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

    # Validation will happen in init method
    @classmethod
    def init_app(cls, app):
        """Validate production configuration."""
        if not cls.SQLALCHEMY_DATABASE_URI:
            raise ValueError("DATABASE_URL environment variable must be set in production")
        if not cls.REDIS_URL:
            raise ValueError("REDIS_URL environment variable must be set in production")
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY environment variable must be set in production")

    # Security Headers (strict)
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
    }

    # Logging
    LOG_LEVEL = 'WARNING'
    LOG_FILE = '/var/log/quiz-app/production.log'

    # Rate limiting (stricter in production)
    RATELIMIT_DEFAULT_LIMITS = ["100 per day", "20 per hour"]


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """
    Get configuration class based on name or environment variable.

    Args:
        config_name: Configuration name (development/testing/staging/production)

    Returns:
        Configuration class
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    return config.get(config_name, DevelopmentConfig)
