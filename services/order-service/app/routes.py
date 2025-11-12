"""Order routes - inter-service communication example"""
from flask import Blueprint, request, jsonify, current_app
from app.models import Order, OrderItem, OrderStatus
from shared.circuit_breaker import order_service_breaker
import logging

logger = logging.getLogger(__name__)
order_bp = Blueprint('orders', __name__)

@order_bp.route('/', methods=['POST'])
@order_service_breaker
def create_order():
    """Create order - demonstrates inter-service communication"""
    data = request.get_json()
    user_id = data.get('user_id')
    items = data.get('items', [])

    db = current_app.db

    try:
        # Verify user exists (call user-service)
        user_response = current_app.user_client.get(f'/api/v1/users/{user_id}')

        total_amount = 0
        order_items = []

        # Verify products and calculate total
        for item in items:
            product_response = current_app.product_client.get(f'/api/v1/products/{item["product_id"]}')
            product = product_response

            item_total = float(product['price']) * item['quantity']
            total_amount += item_total
            order_items.append({
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'price': product['price']
            })

        # Create order
        with db.session_scope() as session:
            order = Order(
                user_id=user_id,
                total_amount=total_amount,
                shipping_address=data.get('shipping_address'),
                status=OrderStatus.PENDING
            )
            session.add(order)
            session.flush()

            # Add order items
            for item_data in order_items:
                item = OrderItem(
                    order_id=order.id,
                    **item_data
                )
                session.add(item)

            result = order.to_dict()
            result['items'] = order_items

        logger.info(f"Order created: {order.id}")
        return jsonify(result), 201

    except Exception as e:
        logger.error(f"Create order error: {str(e)}")
        return jsonify({'error': 'Failed to create order'}), 500

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order by ID"""
    db = current_app.db
    with db.session_scope() as session:
        order = session.query(Order).filter(Order.id == order_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify(order.to_dict()), 200
