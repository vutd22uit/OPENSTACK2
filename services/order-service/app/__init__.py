"""Order Service - Order processing"""
from flask import Flask
from flask_cors import CORS
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from shared.config import get_config
from shared.database import Database
from shared.tracing import init_tracer, instrument_app
from shared.service_client import ServiceClient

def create_app():
    app = Flask(__name__)
    config = get_config()
    CORS(app)

    db = Database(config.DATABASE_URL)
    app.db = db

    # Service clients for inter-service communication
    app.user_client = ServiceClient(os.getenv('USER_SERVICE_URL', 'http://user-service:5001'))
    app.product_client = ServiceClient(os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:5002'))

    if config.ENABLE_TRACING:
        init_tracer('order-service', config.JAEGER_AGENT_HOST, config.JAEGER_AGENT_PORT)
        instrument_app(app)

    from app.routes import order_bp
    app.register_blueprint(order_bp, url_prefix='/api/v1/orders')

    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'order-service'}, 200

    @app.route('/ready')
    def ready():
        return {'status': 'ready', 'database': db.health_check()}, 200

    return app
