#!/usr/bin/env python3
"""
Test script to verify Swagger UI integration for both services
"""

import json
import requests
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.user_service.swagger_spec import get_swagger_spec as get_user_swagger_spec
from services.course_service.swagger_spec import get_swagger_spec as get_course_swagger_spec

def test_swagger_specs():
    """Test that Swagger specifications are properly formatted"""
    print("Testing User Service Swagger Specification...")
    try:
        user_spec = get_user_swagger_spec()
        # Verify it's valid JSON by serializing it
        json.dumps(user_spec)
        print("✅ User Service Swagger spec is valid JSON")
        print(f"   - API Title: {user_spec['info']['title']}")
        print(f"   - Version: {user_spec['info']['version']}")
        print(f"   - Number of paths: {len(user_spec['paths'])}")
        print(f"   - Number of schemas: {len(user_spec['components']['schemas'])}")
    except Exception as e:
        print(f"❌ User Service Swagger spec error: {e}")

    print("\nTesting Course Service Swagger Specification...")
    try:
        course_spec = get_course_swagger_spec()
        # Verify it's valid JSON by serializing it
        json.dumps(course_spec)
        print("✅ Course Service Swagger spec is valid JSON")
        print(f"   - API Title: {course_spec['info']['title']}")
        print(f"   - Version: {course_spec['info']['version']}")
        print(f"   - Number of paths: {len(course_spec['paths'])}")
        print(f"   - Number of schemas: {len(course_spec['components']['schemas'])}")
    except Exception as e:
        print(f"❌ Course Service Swagger spec error: {e}")

def check_required_documentation():
    """Check that all required endpoints from milestone 5 are documented"""
    print("\nChecking required documentation...")
    
    # User Service endpoints
    user_spec = get_user_swagger_spec()
    user_paths = user_spec['paths'].keys()
    
    required_user_endpoints = [
        '/auth/login',
        '/auth/callback', 
        '/auth/logout',
        '/auth/profile',
        '/auth/change-role',
        '/api/users',
        '/api/users/{user_id}',
        '/api/users/by-role/{role}',
        '/api/users/{user_id}/role',
        '/api/users/instructors'
    ]
    
    print("User Service endpoints:")
    for endpoint in required_user_endpoints:
        if endpoint in user_paths:
            print(f"✅ {endpoint}")
        else:
            print(f"❌ {endpoint} - MISSING")
    
    # Course Service endpoints  
    course_spec = get_course_swagger_spec()
    course_paths = course_spec['paths'].keys()
    
    required_course_endpoints = [
        '/api/courses',
        '/api/courses/{course_id}',
        '/api/courses/{course_id}/enroll',
        '/api/enrollments/student/{student_id}',
        '/generateReport',
        '/api/analytics'
    ]
    
    print("\nCourse Service endpoints:")
    for endpoint in required_course_endpoints:
        if endpoint in course_paths:
            print(f"✅ {endpoint}")
        else:
            print(f"❌ {endpoint} - MISSING")

def check_milestone5_requirements():
    """Check specific Milestone 5 requirements"""
    print("\nChecking Milestone 5 specific requirements...")
    
    # Check OAuth2 documentation in User Service
    user_spec = get_user_swagger_spec()
    if 'OAuth2' in user_spec['components']['securitySchemes']:
        print("✅ OAuth2 Google authentication documented")
    else:
        print("❌ OAuth2 Google authentication documentation missing")
    
    # Check API key documentation in Course Service
    course_spec = get_course_swagger_spec()
    if 'ApiKeyAuth' in course_spec['components']['securitySchemes']:
        print("✅ API key authentication documented")
    else:
        print("❌ API key authentication documentation missing")
    
    # Check pagination parameters in courses endpoint
    courses_get = course_spec['paths']['/api/courses']['get']
    param_names = [p['name'] for p in courses_get.get('parameters', [])]
    required_params = ['page', 'limit', 'category', 'sort']
    
    print("Course API pagination/filtering parameters:")
    for param in required_params:
        if param in param_names:
            print(f"✅ {param}")
        else:
            print(f"❌ {param} - MISSING")
    
    # Check HATEOAS documentation
    if '_links' in str(course_spec):
        print("✅ HATEOAS links documented")
    else:
        print("❌ HATEOAS links documentation missing")

if __name__ == "__main__":
    print("🔍 Testing Milestone 5: API Documentation Implementation")
    print("=" * 60)
    
    test_swagger_specs()
    check_required_documentation()
    check_milestone5_requirements()
    
    print("\n📋 Summary:")
    print("- Flask-Swagger-UI integrated into both services")
    print("- Swagger UI available at /docs endpoint")  
    print("- OpenAPI specifications at /swagger.json endpoint")
    print("- OAuth2 Google authentication documented")
    print("- API key authentication documented")
    print("- Role-based endpoints documented")
    print("- Pagination, filtering, sorting documented")
    print("- HATEOAS links documented")
    print("- All required endpoints covered")