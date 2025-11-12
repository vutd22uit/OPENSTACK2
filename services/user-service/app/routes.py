"""
User Service API routes
"""
from flask import Blueprint, request, jsonify, current_app
from app.models import User
from app.auth import generate_token, require_auth
from shared.circuit_breaker import user_service_breaker
import logging

logger = logging.getLogger(__name__)
user_bp = Blueprint('users', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()

        # Validation
        required_fields = ['email', 'username', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        db = current_app.db

        with db.session_scope() as session:
            # Check if user exists
            existing_user = session.query(User).filter(
                (User.email == data['email']) | (User.username == data['username'])
            ).first()

            if existing_user:
                return jsonify({'error': 'User already exists'}), 409

            # Create new user
            user = User(
                email=data['email'],
                username=data['username'],
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )
            user.set_password(data['password'])

            session.add(user)
            session.flush()

            result = user.to_dict()

        logger.info(f"User registered: {user.id}")
        return jsonify(result), 201

    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@user_bp.route('/login', methods=['POST'])
@user_service_breaker
def login():
    """User login"""
    try:
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing credentials'}), 400

        db = current_app.db

        with db.session_scope() as session:
            user = session.query(User).filter(User.username == data['username']).first()

            if not user or not user.check_password(data['password']):
                return jsonify({'error': 'Invalid credentials'}), 401

            if not user.is_active:
                return jsonify({'error': 'Account is disabled'}), 403

            # Generate JWT token
            token = generate_token(user.id, user.username, user.is_admin)

            logger.info(f"User logged in: {user.id}")
            return jsonify({
                'token': token,
                'user': user.to_dict()
            }), 200

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@user_bp.route('/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    """Get user by ID"""
    try:
        db = current_app.db

        with db.session_scope() as session:
            user = session.query(User).filter(User.id == user_id).first()

            if not user:
                return jsonify({'error': 'User not found'}), 404

            return jsonify(user.to_dict()), 200

    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@user_bp.route('/<int:user_id>', methods=['PUT'])
@require_auth
def update_user(user_id):
    """Update user information"""
    try:
        data = request.get_json()
        db = current_app.db

        with db.session_scope() as session:
            user = session.query(User).filter(User.id == user_id).first()

            if not user:
                return jsonify({'error': 'User not found'}), 404

            # Update allowed fields
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'email' in data:
                user.email = data['email']

            session.flush()
            result = user.to_dict()

        logger.info(f"User updated: {user_id}")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Update user error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@user_bp.route('/', methods=['GET'])
@require_auth
def list_users():
    """List all users (paginated)"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)

        if limit > 100:
            limit = 100

        db = current_app.db

        with db.session_scope() as session:
            offset = (page - 1) * limit
            users = session.query(User).offset(offset).limit(limit).all()
            total = session.query(User).count()

            return jsonify({
                'users': [user.to_dict() for user in users],
                'page': page,
                'limit': limit,
                'total': total
            }), 200

    except Exception as e:
        logger.error(f"List users error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
