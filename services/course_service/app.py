from flask import Flask, request, jsonify
from datetime import datetime
import os
from dotenv import load_dotenv
from models.database import db, init_db
from routes.courses import courses_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Database configuration - same PostgreSQL database as main app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/learning_platform')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Session configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Initialize database
    init_db(app)
    
    # Global middleware: Log every request
    @app.before_request
    def log_request():
        """Global middleware to log every request with method, path, and timestamp"""
        timestamp = datetime.now().isoformat()
        print(f"[COURSE-SERVICE {timestamp}] {request.method} {request.path}")
    
    # Register blueprints
    app.register_blueprint(courses_bp, url_prefix='/api')
    
    # Health check route
    @app.route('/')
    def health_check():
        return jsonify({
            'service': 'Course Service',
            'status': 'healthy',
            'message': 'Course management microservice'
        })
    
    # Service info route
    @app.route('/info')
    def service_info():
        return jsonify({
            'service': 'Course Service',
            'version': '1.0.0',
            'description': 'Manages courses and enrollments',
            'endpoints': {
                'courses': '/api/courses/*',
                'enrollments': '/api/enrollments/*',
                'health': '/',
                'info': '/info'
            },
            'dependencies': {
                'user_service': os.getenv('USER_SERVICE_URL', 'http://localhost:5002')
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Course Service runs on port 5003
    app.run(debug=True, host='0.0.0.0', port=5003)