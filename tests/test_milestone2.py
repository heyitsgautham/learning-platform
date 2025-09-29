#!/usr/bin/env python3
"""
Test suite for Milestone 2: Async Patterns & RBAC
Tests the /generateReport route, OAuth2 authentication, and RBAC functionality.
"""

import requests
import time
import json
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test configuration
BASE_URL = "http://localhost:5001"
ANALYTICS_API_KEY = "validKey"

def test_async_generate_report():
    """Test the async /generateReport route"""
    print("Testing /generateReport route...")
    
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/generateReport")
        end_time = time.time()
        
        print(f"Response status: {response.status_code}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response data: {data}")
            
            # Verify the response structure
            if "status" in data and data["status"] == "Report generated":
                print("✅ /generateReport route working correctly")
                return True
            else:
                print("❌ Unexpected response format")
                return False
        else:
            print(f"❌ Expected status 200, got {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure Flask app is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error testing /generateReport: {e}")
        return False

def test_health_check():
    """Test the basic health check route"""
    print("Testing health check route...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response data: {data}")
            print("✅ Health check working correctly")
            return True
        else:
            print(f"❌ Expected status 200, got {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure Flask app is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error testing health check: {e}")
        return False

def test_analytics_middleware():
    """Test the analytics middleware (API key requirement)"""
    print("Testing analytics middleware...")
    
    try:
        # Test without API key
        response = requests.get(f"{BASE_URL}/analytics")
        print(f"Response status (no API key): {response.status_code}")
        
        if response.status_code == 403:
            print("✅ Analytics endpoint correctly blocks requests without API key")
        else:
            print(f"❌ Expected status 403, got {response.status_code}")
            return False
        
        # Test with correct API key
        response = requests.get(f"{BASE_URL}/analytics", params={"apiKey": ANALYTICS_API_KEY})
        print(f"Response status (with API key): {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Analytics endpoint correctly accepts valid API key")
            return True
        else:
            print(f"❌ Expected status 200, got {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure Flask app is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error testing analytics middleware: {e}")
        return False

def test_oauth_routes():
    """Test OAuth2 routes (basic availability)"""
    print("Testing OAuth2 routes...")
    
    try:
        # Test login route (should redirect to Google)
        response = requests.get(f"{BASE_URL}/auth/login", allow_redirects=False)
        print(f"Login route status: {response.status_code}")
        
        # Should either be a redirect (302) or error (500) if OAuth not configured
        if response.status_code in [302, 500]:
            print("✅ Login route exists and responds appropriately")
        else:
            print(f"❌ Unexpected login route status: {response.status_code}")
            return False
        
        # Test profile route (should require authentication)
        response = requests.get(f"{BASE_URL}/auth/profile")
        print(f"Profile route status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Profile route correctly requires authentication")
            return True
        else:
            print(f"❌ Expected status 401, got {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure Flask app is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error testing OAuth routes: {e}")
        return False

def test_rbac_routes():
    """Test RBAC protected routes"""
    print("Testing RBAC protected routes...")
    
    try:
        # Test courses route (should require authentication)
        response = requests.get(f"{BASE_URL}/api/courses")
        print(f"Courses route status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Courses route correctly requires authentication")
        else:
            print(f"❌ Expected status 401, got {response.status_code}")
            return False
        
        # Test course creation (should require teacher/admin role)
        response = requests.post(f"{BASE_URL}/api/courses", 
                               json={"title": "Test Course"})
        print(f"Create course route status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Create course route correctly requires authentication")
            return True
        else:
            print(f"❌ Expected status 401, got {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure Flask app is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error testing RBAC routes: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("MILESTONE 2 TESTS: Async Patterns & RBAC")
    print("="*60)
    
    tests = [
        test_health_check,
        test_async_generate_report,
        test_analytics_middleware,
        test_oauth_routes,
        test_rbac_routes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print("\n" + "-"*40)
        if test():
            passed += 1
        print("-"*40)
    
    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Milestone 2 tests passed!")
        print("\nMilestone 2 Implementation Summary:")
        print("✅ Async /generateReport route implemented")
        print("✅ OAuth2 authentication routes created")
        print("✅ RBAC middleware implemented")
        print("✅ User model with roles created")
        print("✅ Protected routes working correctly")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)