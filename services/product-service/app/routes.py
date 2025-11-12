"""Product routes"""
from flask import Blueprint, request, jsonify, current_app
from app.models import Product
import logging

logger = logging.getLogger(__name__)
product_bp = Blueprint('products', __name__)

@product_bp.route('/', methods=['GET'])
def list_products():
    """List products with pagination"""
    page = request.args.get('page', 1, type=int)
    limit = min(request.args.get('limit', 10, type=int), 100)

    db = current_app.db
    with db.session_scope() as session:
        offset = (page - 1) * limit
        products = session.query(Product).offset(offset).limit(limit).all()
        total = session.query(Product).count()

        return jsonify({
            'products': [p.to_dict() for p in products],
            'page': page,
            'limit': limit,
            'total': total
        }), 200

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    db = current_app.db
    with db.session_scope() as session:
        product = session.query(Product).filter(Product.id == product_id).first()
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product.to_dict()), 200

@product_bp.route('/', methods=['POST'])
def create_product():
    """Create new product"""
    data = request.get_json()
    db = current_app.db

    with db.session_scope() as session:
        product = Product(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            stock_quantity=data.get('stock_quantity', 0),
            sku=data['sku'],
            category=data.get('category')
        )
        session.add(product)
        session.flush()
        result = product.to_dict()

    return jsonify(result), 201
