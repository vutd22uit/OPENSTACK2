"""Product Service - Product catalog and inventory management"""
from flask import Flask
from flask_cors import CORS
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from shared.config import get_config
from shared.database import Database
from shared.tracing import init_tracer, instrument_app

def create_app():
    app = Flask(__name__)
    config = get_config()
    CORS(app)
    db = Database(config.DATABASE_URL)
    app.db = db

    if config.ENABLE_TRACING:
        init_tracer('product-service', config.JAEGER_AGENT_HOST, config.JAEGER_AGENT_PORT)
        instrument_app(app)

    from app.routes import product_bp
    app.register_blueprint(product_bp, url_prefix='/api/v1/products')

    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'product-service'}, 200

    @app.route('/ready')
    def ready():
        return {'status': 'ready', 'database': db.health_check()}, 200

    return app
