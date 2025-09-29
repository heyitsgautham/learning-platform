from flask import Flask, request, jsonify
from datetime import datetime
import os
from dotenv import load_dotenv
from models.database import db, init_db
from routes.auth import auth_bp, init_oauth
from routes.users import users_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Database configuration - same PostgreSQL database as main app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/learning_platform')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Session configuration for OAuth
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    
    # Google OAuth configuration
    app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
    app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
    
    # Initialize database
    init_db(app)
    
    # Initialize OAuth
    oauth, google = init_oauth(app)
    auth_bp.oauth = oauth
    auth_bp.google = google
    
    # Global middleware: Log every request
    @app.before_request
    def log_request():
        """Global middleware to log every request with method, path, and timestamp"""
        timestamp = datetime.now().isoformat()
        print(f"[USER-SERVICE {timestamp}] {request.method} {request.path}")
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/api')
    
    # Health check route
    @app.route('/')
    def health_check():
        return jsonify({
            'service': 'User Service',
            'status': 'healthy',
            'message': 'User management microservice'
        })
    
    # Service info route
    @app.route('/info')
    def service_info():
        return jsonify({
            'service': 'User Service',
            'version': '1.0.0',
            'description': 'Manages users, authentication, and roles',
            'endpoints': {
                'auth': '/auth/*',
                'users': '/api/users/*',
                'health': '/',
                'info': '/info'
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    # User Service runs on port 5002
    app.run(debug=True, host='0.0.0.0', port=5002)