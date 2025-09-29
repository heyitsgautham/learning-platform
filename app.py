from flask import Flask, request, jsonify, g, session
from datetime import datetime
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from models.database import db, init_db
from routes.analytics import analytics_bp
from routes.auth import auth_bp, init_oauth
from routes.courses import courses_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Database configuration
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
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(courses_bp, url_prefix='/api')
    
    # Basic health check route
    @app.route('/')
    def health_check():
        return jsonify({'message': 'Smart Learning Platform API', 'status': 'healthy'})
    
    # Async generateReport route
    @app.route('/generateReport', methods=['GET'])
    def generate_report():
        """
        Simulate a long-running task using asyncio to prevent blocking other requests.
        This demonstrates async patterns in the Flask application.
        """
        async def process_report():
            # Simulate long-running task (e.g., processing assignments)
            await asyncio.sleep(3)  # 3 second delay to simulate processing
            return {"status": "Report generated", "timestamp": datetime.now().isoformat()}
        
        # Run the async task in a thread pool to prevent blocking Flask
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(process_report())
            return jsonify(result)
        finally:
            loop.close()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)