"""
Application entry point for Flask Quiz App.

This file is used to run the Flask development server.
For production, use Gunicorn or another WSGI server.
"""

import os
from app import create_app

# Create application instance
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 'yes']
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')

    # Run development server
    app.run(host=host, port=port, debug=debug)
