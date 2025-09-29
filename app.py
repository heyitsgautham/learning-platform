from flask import Flask, request, jsonify, g
from datetime import datetime
import os
from dotenv import load_dotenv
from models.database import db, init_db
from routes.analytics import analytics_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/learning_platform')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    init_db(app)
    
    # Global middleware: Log every request
    @app.before_request
    def log_request():
        """Global middleware to log every request with method, path, and timestamp"""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] {request.method} {request.path}")
    
    # Route-specific middleware for analytics
    @app.before_request
    def validate_analytics_api_key():
        """Route-specific middleware for /analytics endpoint"""
        if request.path == '/analytics':
            api_key = request.args.get('apiKey')
            expected_key = os.getenv('ANALYTICS_API_KEY', 'validKey')
            
            if not api_key or api_key != expected_key:
                return jsonify({'error': 'Invalid or missing API key'}), 403
    
    # Register blueprints
    app.register_blueprint(analytics_bp)
    
    # Basic health check route
    @app.route('/')
    def health_check():
        return jsonify({'message': 'Smart Learning Platform API', 'status': 'healthy'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)