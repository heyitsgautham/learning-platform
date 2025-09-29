from flask import Flask, request, jsonify
from datetime import datetime
import os
import asyncio
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint
from models.database import db, init_db
from routes.courses import courses_bp
from swagger_spec import get_swagger_spec

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
    
    # Swagger UI configuration
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'
    
    # Create Swagger UI blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Course Service API",
            'supportedSubmitMethods': ['get', 'post', 'put', 'delete'],
            'docExpansion': 'list',
            'defaultModelsExpandDepth': 2,
            'defaultModelExpandDepth': 2,
            'swagger_ui_parameters': {'topbar': False}
        }
    )
    
    # Register Swagger UI blueprint (no url_prefix needed since it's already in SWAGGER_URL)
    app.register_blueprint(swaggerui_blueprint)
    
    # Swagger spec endpoint
    @app.route('/swagger.json')
    def swagger_spec():
        """Return the OpenAPI specification"""
        return jsonify(get_swagger_spec())
    
    # Global middleware: Log every request
    @app.before_request
    def log_request():
        """Global middleware to log every request with method, path, and timestamp"""
        timestamp = datetime.now().isoformat()
        print(f"[COURSE-SERVICE {timestamp}] {request.method} {request.path}")
    
    # Register blueprints
    app.register_blueprint(courses_bp, url_prefix='/api')
    
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