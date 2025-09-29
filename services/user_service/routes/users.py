from flask import Blueprint, request, jsonify
from models.database import db, User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify({
        'users': [user.to_dict() for user in users],
        'total': len(users)
    })

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    user = User.query.get_or_404(user_id)
    return jsonify({'user': user.to_dict()})

@users_bp.route('/users/by-role/<role>', methods=['GET'])
def get_users_by_role(role):
    """Get users by role (student, teacher, admin)"""
    if role not in ['student', 'teacher', 'admin']:
        return jsonify({'error': 'Invalid role. Must be student, teacher, or admin'}), 400
    
    users = User.query.filter_by(role=role).all()
    return jsonify({
        'users': [user.to_dict() for user in users],
        'role': role,
        'total': len(users)
    })

@users_bp.route('/users/<int:user_id>/role', methods=['PUT'])
def update_user_role(user_id):
    """Update user role"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data or 'role' not in data:
        return jsonify({'error': 'Role is required'}), 400
    
    new_role = data['role']
    if new_role not in ['student', 'teacher', 'admin']:
        return jsonify({'error': 'Invalid role. Must be student, teacher, or admin'}), 400
    
    user.role = new_role
    db.session.commit()
    
    return jsonify({
        'message': f'User role updated to {new_role}',
        'user': user.to_dict()
    })

@users_bp.route('/users/instructors', methods=['GET'])
def get_instructors():
    """Get all users with teacher role (instructors)"""
    instructors = User.query.filter_by(role='teacher').all()
    return jsonify({
        'instructors': [user.to_dict() for user in instructors],
        'total': len(instructors)
    })