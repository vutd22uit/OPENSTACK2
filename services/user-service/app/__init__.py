"""
User Service - Handles user authentication and management
"""
from flask import Flask
from flask_cors import CORS
import logging
import sys
import os

# Add shared library to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from shared.config import get_config
from shared.database import Database
from shared.tracing import init_tracer, instrument_app
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

logger = logging.getLogger(__name__)


def create_app():
    """Application factory"""
    app = Flask(__name__)

    # Load configuration
    config = get_config()
    app.config['SERVICE_NAME'] = 'user-service'

    # CORS
    CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS.split(',')}})

    # Database
    db = Database(config.DATABASE_URL, config.DB_POOL_SIZE, config.DB_MAX_OVERFLOW)
    app.db = db

    # Distributed tracing
    if config.ENABLE_TRACING:
        init_tracer('user-service', config.JAEGER_AGENT_HOST, config.JAEGER_AGENT_PORT)
        instrument_app(app)

    # Prometheus metrics
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })

    # Register blueprints
    from app.routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')

    # Health checks
    @app.route('/health')
    def health():
        """Liveness probe"""
        return {'status': 'healthy', 'service': 'user-service'}, 200

    @app.route('/ready')
    def ready():
        """Readiness probe - check dependencies"""
        checks = {
            'database': db.health_check(),
        }

        if all(checks.values()):
            return {'status': 'ready', 'checks': checks}, 200
        else:
            return {'status': 'not_ready', 'checks': checks}, 503

    logger.info("User service initialized")
    return app
