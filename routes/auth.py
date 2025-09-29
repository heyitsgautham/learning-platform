from flask import Blueprint, request, jsonify, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from models.database import db, User
import os

auth_bp = Blueprint('auth', __name__)

def init_oauth(app):
    """Initialize OAuth configuration"""
    oauth = OAuth(app)
    
    # Check if OAuth credentials are configured
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("WARNING: Google OAuth credentials not configured. OAuth features will be disabled.")
        return oauth, None
    
    # Configure Google OAuth with explicit endpoints
    google = oauth.register(
        name='google',
        client_id=client_id,
        client_secret=client_secret,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        access_token_url='https://oauth2.googleapis.com/token',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    
    return oauth, google

@auth_bp.route('/login')
def login():
    """Initiate Google OAuth login"""
    if not hasattr(auth_bp, 'google') or auth_bp.google is None:
        return jsonify({'error': 'OAuth not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables.'}), 500
    
    redirect_uri = url_for('auth.auth_callback', _external=True)
    return auth_bp.google.authorize_redirect(redirect_uri)

@auth_bp.route('/callback')
def auth_callback():
    """Handle OAuth callback from Google"""
    if not hasattr(auth_bp, 'google') or auth_bp.google is None:
        return jsonify({'error': 'OAuth not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables.'}), 500
    
    try:
        token = auth_bp.google.authorize_access_token()
        
        # Get user info from Google
        user_info_resp = auth_bp.google.get('https://www.googleapis.com/oauth2/v2/userinfo', token=token)
        user_info = user_info_resp.json()
        
        if user_info:
            # Check if user exists, create if not
            user = User.query.filter_by(google_id=user_info['id']).first()
            
            if not user:
                # Create new user with default role 'student'
                user = User(
                    email=user_info['email'],
                    google_id=user_info['id'],
                    name=user_info['name'],
                    role='student'  # Default role
                )
                db.session.add(user)
                db.session.commit()
            
            # Store user in session
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_role'] = user.role
            
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict()
            })
        else:
            return jsonify({'error': 'Failed to get user info'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Authentication failed: {str(e)}'}), 400

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user by clearing session"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@auth_bp.route('/profile')
def profile():
    """Get current user profile"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()})

@auth_bp.route('/users/<int:user_id>/role', methods=['PUT'])
def update_user_role(user_id):
    """Update user role (admin only)"""
    # Check if user is authenticated and is admin
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    current_user = User.query.get(session['user_id'])
    if not current_user or current_user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    # Get target user
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get new role from request
    data = request.get_json()
    new_role = data.get('role')
    
    if new_role not in ['student', 'teacher', 'admin']:
        return jsonify({'error': 'Invalid role. Must be student, teacher, or admin'}), 400
    
    # Update role
    target_user.role = new_role
    db.session.commit()
    
    return jsonify({
        'message': f'User role updated to {new_role}',
        'user': target_user.to_dict()
    })