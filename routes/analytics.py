from flask import Blueprint, jsonify

# Create analytics blueprint
analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics', methods=['GET'])
def analytics():
    """
    Analytics endpoint that requires valid API key.
    The API key validation is handled by middleware in app.py
    """
    return jsonify({'message': 'Analytics access granted'})