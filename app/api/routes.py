"""
API Routes with security validations
"""
from flask import Blueprint, request, jsonify
from app.services.data_service import DataService
from app.utils.validators import validate_input, sanitize_input
import logging

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)
data_service = DataService()

@api_bp.route('/status', methods=['GET'])
def get_status():
    """Get API status"""
    return jsonify({
        'status': 'operational',
        'message': 'API is running'
    }), 200

@api_bp.route('/data', methods=['GET'])
def get_data():
    """Get data with pagination and validation"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)

        # Input validation
        if page < 1 or limit < 1 or limit > 100:
            return jsonify({'error': 'Invalid pagination parameters'}), 400

        data = data_service.get_paginated_data(page, limit)
        return jsonify(data), 200

    except Exception as e:
        logger.error(f"Error in get_data: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/data', methods=['POST'])
def create_data():
    """Create new data with input validation and sanitization"""
    try:
        # Get and validate input
        input_data = request.get_json()

        if not input_data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        required_fields = ['name', 'description']
        if not all(field in input_data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Sanitize input to prevent XSS
        sanitized_data = {
            'name': sanitize_input(input_data['name']),
            'description': sanitize_input(input_data['description'])
        }

        # Additional validation
        if not validate_input(sanitized_data['name'], max_length=100):
            return jsonify({'error': 'Invalid name format'}), 400

        result = data_service.create_data(sanitized_data)
        return jsonify(result), 201

    except Exception as e:
        logger.error(f"Error in create_data: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/data/<int:data_id>', methods=['GET'])
def get_data_by_id(data_id):
    """Get specific data by ID with validation"""
    try:
        if data_id < 1:
            return jsonify({'error': 'Invalid ID'}), 400

        data = data_service.get_by_id(data_id)

        if not data:
            return jsonify({'error': 'Data not found'}), 404

        return jsonify(data), 200

    except Exception as e:
        logger.error(f"Error in get_data_by_id: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@api_bp.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500
