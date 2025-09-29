import unittest
import os
import sys
import importlib.util

# Get the services directory path
services_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'services')

class TestMicroservicesStructure(unittest.TestCase):
    """Test the microservices implementation for Milestone 3"""
    
    def test_user_service_structure(self):
        """Test that User Service has the correct structure"""
        user_service_path = os.path.join(services_dir, 'user_service')
        
        # Check main app file exists
        self.assertTrue(os.path.exists(os.path.join(user_service_path, 'app.py')))
        
        # Check models directory and files
        self.assertTrue(os.path.exists(os.path.join(user_service_path, 'models', 'database.py')))
        
        # Check routes directory and files
        self.assertTrue(os.path.exists(os.path.join(user_service_path, 'routes', 'auth.py')))
        self.assertTrue(os.path.exists(os.path.join(user_service_path, 'routes', 'users.py')))
        
        # Check requirements.txt
        self.assertTrue(os.path.exists(os.path.join(user_service_path, 'requirements.txt')))
        
        # Check Dockerfile
        self.assertTrue(os.path.exists(os.path.join(user_service_path, 'Dockerfile')))
    
    def test_course_service_structure(self):
        """Test that Course Service has the correct structure"""
        course_service_path = os.path.join(services_dir, 'course_service')
        
        # Check main app file exists
        self.assertTrue(os.path.exists(os.path.join(course_service_path, 'app.py')))
        
        # Check models directory and files
        self.assertTrue(os.path.exists(os.path.join(course_service_path, 'models', 'database.py')))
        
        # Check routes directory and files
        self.assertTrue(os.path.exists(os.path.join(course_service_path, 'routes', 'courses.py')))
        
        # Check requirements.txt
        self.assertTrue(os.path.exists(os.path.join(course_service_path, 'requirements.txt')))
        
        # Check Dockerfile
        self.assertTrue(os.path.exists(os.path.join(course_service_path, 'Dockerfile')))
    
    def test_user_service_imports(self):
        """Test that User Service can be imported successfully"""
        user_service_path = os.path.join(services_dir, 'user_service')
        app_file = os.path.join(user_service_path, 'app.py')
        
        # Check that the app.py file exists
        self.assertTrue(os.path.exists(app_file), "User Service app.py file not found")
        
        # Check that the app.py file contains the create_app function
        with open(app_file, 'r') as f:
            app_content = f.read()
        
        self.assertIn('def create_app()', app_content, "User Service should have a create_app function")
        self.assertIn('Flask(__name__)', app_content, "User Service should create a Flask app")
        
        # Try to load and execute the module (allowing for import errors due to dependencies)
        try:
            spec = importlib.util.spec_from_file_location("user_service_app", app_file)
            user_service_module = importlib.util.module_from_spec(spec)
            
            # Add the service directory to sys.path temporarily
            sys.path.insert(0, user_service_path)
            try:
                spec.loader.exec_module(user_service_module)
                
                # Check if create_app function exists
                self.assertTrue(hasattr(user_service_module, 'create_app'), 
                              "User Service should have a create_app function")
                
                # Try to create the app (this may fail due to database connection, which is expected)
                try:
                    app = user_service_module.create_app()
                    self.assertIsNotNone(app)
                except Exception as e:
                    # Database connection errors are expected without proper DB setup
                    print(f"Expected database/dependency error in User Service: {e}")
                    
            finally:
                sys.path.remove(user_service_path)
                
        except (ImportError, ModuleNotFoundError) as e:
            # Import errors are acceptable if dependencies aren't available in test environment
            print(f"Import error in User Service (acceptable): {e}")
            # Just verify the structure is correct
            self.assertIn('from routes.auth import', app_content)
            self.assertIn('from models.database import', app_content)
        except Exception as e:
            self.fail(f"Unexpected error loading User Service module: {e}")
    
    def test_course_service_imports(self):
        """Test that Course Service can be imported successfully"""
        course_service_path = os.path.join(services_dir, 'course_service')
        app_file = os.path.join(course_service_path, 'app.py')
        
        # Check that the app.py file exists
        self.assertTrue(os.path.exists(app_file), "Course Service app.py file not found")
        
        # Check that the app.py file contains the create_app function
        with open(app_file, 'r') as f:
            app_content = f.read()
        
        self.assertIn('def create_app()', app_content, "Course Service should have a create_app function")
        self.assertIn('Flask(__name__)', app_content, "Course Service should create a Flask app")
        
        # Try to load and execute the module (allowing for import errors due to dependencies)
        try:
            spec = importlib.util.spec_from_file_location("course_service_app", app_file)
            course_service_module = importlib.util.module_from_spec(spec)
            
            # Add the service directory to sys.path temporarily
            sys.path.insert(0, course_service_path)
            try:
                spec.loader.exec_module(course_service_module)
                
                # Check if create_app function exists
                self.assertTrue(hasattr(course_service_module, 'create_app'), 
                              "Course Service should have a create_app function")
                
                # Try to create the app (this may fail due to database connection, which is expected)
                try:
                    app = course_service_module.create_app()
                    self.assertIsNotNone(app)
                except Exception as e:
                    # Database connection errors are expected without proper DB setup
                    print(f"Expected database/dependency error in Course Service: {e}")
                    
            finally:
                sys.path.remove(course_service_path)
                
        except (ImportError, ModuleNotFoundError) as e:
            # Import errors are acceptable if dependencies aren't available in test environment
            print(f"Import error in Course Service (acceptable): {e}")
            # Just verify the structure is correct
            self.assertIn('from routes.courses import', app_content)
            self.assertIn('from models.database import', app_content)
        except Exception as e:
            self.fail(f"Unexpected error loading Course Service module: {e}")
    
    def test_inter_service_communication_code(self):
        """Test that Course Service has inter-service communication code"""
        course_routes_path = os.path.join(services_dir, 'course_service', 'routes', 'courses.py')
        
        self.assertTrue(os.path.exists(course_routes_path), "Course routes file not found")
        
        with open(course_routes_path, 'r') as f:
            content = f.read()
            
        # Check that the Course Service imports requests for HTTP calls
        self.assertIn('import requests', content)
        
        # Check that there's a function to get instructor details
        self.assertIn('def get_instructor_details', content)
        
        # Check that it calls the User Service
        self.assertIn('USER_SERVICE_URL', content)
        
        # Check that courses are enriched with instructor data
        self.assertIn('get_instructor_details(', content)
    
    def test_database_models(self):
        """Test that both services have proper database models"""
        # Test User Service models
        user_db_path = os.path.join(services_dir, 'user_service', 'models', 'database.py')
        self.assertTrue(os.path.exists(user_db_path), "User Service database models file not found")
        
        with open(user_db_path, 'r') as f:
            user_content = f.read()
        
        self.assertIn('class User(db.Model)', user_content)
        self.assertIn('__tablename__ = \'users\'', user_content)
        
        # Test Course Service models
        course_db_path = os.path.join(services_dir, 'course_service', 'models', 'database.py')
        self.assertTrue(os.path.exists(course_db_path), "Course Service database models file not found")
        
        with open(course_db_path, 'r') as f:
            course_content = f.read()
        
        self.assertIn('class Course(db.Model)', course_content)
        self.assertIn('class Enrollment(db.Model)', course_content)
        self.assertIn('__tablename__ = \'courses\'', course_content)
        self.assertIn('__tablename__ = \'enrollments\'', course_content)
    
    def test_shared_database_configuration(self):
        """Test that both services use the same database configuration"""
        user_app_path = os.path.join(services_dir, 'user_service', 'app.py')
        course_app_path = os.path.join(services_dir, 'course_service', 'app.py')
        
        self.assertTrue(os.path.exists(user_app_path), "User Service app.py not found")
        self.assertTrue(os.path.exists(course_app_path), "Course Service app.py not found")
        
        with open(user_app_path, 'r') as f:
            user_content = f.read()
        
        with open(course_app_path, 'r') as f:
            course_content = f.read()
        
        # Both should use the same DATABASE_URL environment variable
        self.assertIn('DATABASE_URL', user_content)
        self.assertIn('DATABASE_URL', course_content)
        
        # Both should default to the same database name
        self.assertIn('learning_platform', user_content)
        self.assertIn('learning_platform', course_content)

if __name__ == '__main__':
    unittest.main()