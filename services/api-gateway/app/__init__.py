"""API Gateway - Entry point for all client requests"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from shared.config import get_config
from shared.service_client import ServiceClient
from shared.tracing import init_tracer, instrument_app
import logging

logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    config = get_config()

    CORS(app)

    # Rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=config.REDIS_URL
    )

    # Service clients
    app.user_client = ServiceClient(os.getenv('USER_SERVICE_URL', 'http://user-service:5001'))
    app.product_client = ServiceClient(os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:5002'))
    app.order_client = ServiceClient(os.getenv('ORDER_SERVICE_URL', 'http://order-service:5003'))

    if config.ENABLE_TRACING:
        init_tracer('api-gateway', config.JAEGER_AGENT_HOST, config.JAEGER_AGENT_PORT)
        instrument_app(app)

    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'api-gateway'}, 200

    # Proxy routes
    @app.route('/api/v1/users/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    @limiter.limit("10 per minute")
    def proxy_users(path):
        """Proxy to user service"""
        try:
            if request.method == 'GET':
                response = app.user_client.get(f'/api/v1/users/{path}')
            elif request.method == 'POST':
                response = app.user_client.post(f'/api/v1/users/{path}', request.get_json())
            # Add other methods as needed
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"User service error: {str(e)}")
            return jsonify({'error': 'Service unavailable'}), 503

    @app.route('/api/v1/products/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def proxy_products(path):
        """Proxy to product service"""
        try:
            if request.method == 'GET':
                response = app.product_client.get(f'/api/v1/products/{path}')
            elif request.method == 'POST':
                response = app.product_client.post(f'/api/v1/products/{path}', request.get_json())
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Product service error: {str(e)}")
            return jsonify({'error': 'Service unavailable'}), 503

    @app.route('/api/v1/orders/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def proxy_orders(path):
        """Proxy to order service"""
        try:
            if request.method == 'GET':
                response = app.order_client.get(f'/api/v1/orders/{path}')
            elif request.method == 'POST':
                response = app.order_client.post(f'/api/v1/orders/{path}', request.get_json())
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Order service error: {str(e)}")
            return jsonify({'error': 'Service unavailable'}), 503

    logger.info("API Gateway initialized")
    return app
