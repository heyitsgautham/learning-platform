from functools import wraps
from flask import session, jsonify, request
from models.database import User

def require_auth(f):
    """Decorator to require user authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_role(required_role):
    """Decorator to require specific user role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            user = User.query.get(session['user_id'])
            if not user:
                session.clear()
                return jsonify({'error': 'User not found'}), 404
            
            if user.role != required_role:
                return jsonify({'error': f'Access denied. {required_role.title()} role required'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_roles(allowed_roles):
    """Decorator to require one of multiple roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            user = User.query.get(session['user_id'])
            if not user:
                session.clear()
                return jsonify({'error': 'User not found'}), 404
            
            if user.role not in allowed_roles:
                roles_str = ', '.join(allowed_roles)
                return jsonify({'error': f'Access denied. Required roles: {roles_str}'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Get current authenticated user"""
    if 'user_id' not in session:
        return None
    
    return User.query.get(session['user_id'])