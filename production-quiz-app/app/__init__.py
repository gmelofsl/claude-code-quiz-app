"""
Application factory for Flask Quiz App.

This module implements the application factory pattern, which allows
creating multiple instances of the app with different configurations.
"""

import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template

from app.config import get_config
from app.extensions import db, migrate, login_manager, csrf, limiter, cache


def create_app(config_name=None):
    """
    Application factory function.

    Args:
        config_name: Configuration name (development/testing/staging/production)
                    If None, uses FLASK_ENV environment variable

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Initialize extensions
    initialize_extensions(app)

    # Register blueprints
    register_blueprints(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    # Add security headers
    configure_security_headers(app)

    # Initialize Sentry if configured
    initialize_sentry(app)

    # Context processors (make variables available to all templates)
    register_context_processors(app)

    return app


def initialize_extensions(app):
    """Initialize Flask extensions."""
    # Database
    db.init_app(app)

    # Import models so SQLAlchemy can create tables
    # This must happen after db.init_app() but before migrate.init_app()
    from app.models import User, Quiz, Question, Attempt, UserAnswer  # noqa: F401

    # Migrations
    migrate.init_app(app, db)

    # Login manager
    login_manager.init_app(app)

    # CSRF protection
    csrf.init_app(app)

    # Rate limiting
    limiter.init_app(app)

    # Caching
    cache.init_app(app)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login."""
        from app.models.user import User
        return User.query.get(int(user_id))


def register_blueprints(app):
    """Register Flask blueprints."""
    # Import blueprints here to avoid circular imports
    from app.routes.auth import auth_bp

    # Register authentication blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # TODO: Register other blueprints
    # from app.routes.quiz import quiz_bp
    # from app.routes.dashboard import dashboard_bp
    # from app.routes.history import history_bp
    # from app.routes.api import api_bp

    # app.register_blueprint(quiz_bp, url_prefix='/quiz')
    # app.register_blueprint(dashboard_bp)
    # app.register_blueprint(history_bp)
    # app.register_blueprint(api_bp, url_prefix='/api')

    # Temporary root route for testing
    @app.route('/')
    def index():
        return {'status': 'ok', 'message': 'Production Quiz App - Authentication System Active'}

    # Health check endpoint
    @app.route('/health')
    def health_check():
        """
        Health check endpoint for monitoring and load balancers.

        Checks database connectivity and returns system status.
        """
        from datetime import datetime

        health_status = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'quiz-app',
            'version': '1.0.0'
        }

        # Check database connection
        try:
            from sqlalchemy import text
            with db.engine.connect() as conn:
                conn.execute(text('SELECT 1'))
            health_status['database'] = 'connected'
        except Exception as e:
            health_status['database'] = 'disconnected'
            health_status['status'] = 'unhealthy'
            app.logger.error(f'Health check database error: {e}')

        # Check cache connection if configured
        try:
            if cache.cache:
                cache.cache.get('health_check')
                health_status['cache'] = 'connected'
        except Exception as e:
            health_status['cache'] = 'disconnected'
            app.logger.warning(f'Health check cache error: {e}')

        status_code = 200 if health_status['status'] == 'healthy' else 503
        return health_status, status_code


def configure_logging(app):
    """Configure application logging."""
    if not app.debug and not app.testing:
        # Set log level
        log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
        app.logger.setLevel(log_level)

        # File handler if log file is configured
        log_file = app.config.get('LOG_FILE')
        if log_file:
            # Ensure log directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir, exist_ok=True)
                except (OSError, PermissionError):
                    # If can't create log directory, fall back to app directory
                    log_file = 'app.log'

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=app.config.get('LOG_MAX_BYTES', 10485760),
                backupCount=app.config.get('LOG_BACKUP_COUNT', 10)
            )
            file_handler.setFormatter(logging.Formatter(
                '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
            ))
            file_handler.setLevel(log_level)
            app.logger.addHandler(file_handler)

        app.logger.info('Quiz App startup')


def register_error_handlers(app):
    """Register error handlers for common HTTP errors."""

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request."""
        if app.config.get('DEBUG'):
            return {'error': 'Bad Request', 'message': str(error)}, 400
        return render_template_or_json('errors/400.html', error=error), 400

    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized."""
        if app.config.get('DEBUG'):
            return {'error': 'Unauthorized', 'message': str(error)}, 401
        return render_template_or_json('errors/401.html', error=error), 401

    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden."""
        if app.config.get('DEBUG'):
            return {'error': 'Forbidden', 'message': str(error)}, 403
        return render_template_or_json('errors/403.html', error=error), 403

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found."""
        if app.config.get('DEBUG'):
            return {'error': 'Not Found', 'message': str(error)}, 404
        return render_template_or_json('errors/404.html', error=error), 404

    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle 429 Too Many Requests (rate limiting)."""
        return render_template_or_json('errors/429.html', error=error), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        app.logger.error(f'Internal Server Error: {error}')
        if app.config.get('DEBUG'):
            return {'error': 'Internal Server Error', 'message': str(error)}, 500
        return render_template_or_json('errors/500.html', error=error), 500

    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle 503 Service Unavailable."""
        return render_template_or_json('errors/503.html', error=error), 503


def render_template_or_json(template_name, error=None, **kwargs):
    """
    Render template if it exists, otherwise return JSON.

    This allows the app to work even if error templates aren't created yet.
    """
    try:
        return render_template(template_name, error=error, **kwargs)
    except Exception:
        error_code = template_name.split('/')[-1].replace('.html', '')
        return {
            'error': f'Error {error_code}',
            'message': str(error) if error else 'An error occurred'
        }


def configure_security_headers(app):
    """Add security headers to all responses."""

    @app.after_request
    def set_security_headers(response):
        """Set security headers on every response."""
        security_headers = app.config.get('SECURITY_HEADERS', {})

        for header, value in security_headers.items():
            response.headers[header] = value

        return response


def initialize_sentry(app):
    """Initialize Sentry error tracking if configured."""
    sentry_dsn = app.config.get('SENTRY_DSN')

    if sentry_dsn and not app.config.get('TESTING'):
        try:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration

            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[FlaskIntegration()],
                traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
                profiles_sample_rate=0.1,  # 10% for profiling
                environment=app.config.get('FLASK_ENV', 'development'),
            )

            app.logger.info('Sentry error tracking initialized')
        except ImportError:
            app.logger.warning('Sentry SDK not installed, error tracking disabled')
        except Exception as e:
            app.logger.error(f'Failed to initialize Sentry: {e}')


def register_context_processors(app):
    """Register context processors to make variables available to all templates."""

    @app.context_processor
    def inject_config():
        """Make config available to templates."""
        return {
            'app_name': 'AI Development Quiz',
            'debug': app.config.get('DEBUG', False),
        }
