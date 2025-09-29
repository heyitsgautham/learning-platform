#!/usr/bin/env python3
"""
Test script for Milestone 1 implementation
Tests the middleware and basic functionality
"""

import requests
import time
import sys
import os

def test_milestone1():
    # Use environment variable for base URL if available (for CI flexibility)
    base_url = os.getenv('FLASK_BASE_URL', 'http://localhost:5001')
    
    print("🧪 Testing Milestone 1 Implementation")
    print("=" * 50)
    print(f"Testing against: {base_url}")
    
    test_results = []
    
    # Test 1: Health check endpoint
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            test_results.append(True)
        else:
            print(f"❌ Health check failed: {response.status_code}")
            test_results.append(False)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask app is running.")
        test_results.append(False)
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Server may be overloaded.")
        test_results.append(False)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        test_results.append(False)
    
    # Test 2: Analytics endpoint without API key (should fail)
    print("\n2. Testing analytics endpoint without API key...")
    try:
        response = requests.get(f"{base_url}/analytics", timeout=10)
        if response.status_code == 403:
            print("✅ Analytics endpoint correctly rejected request without API key")
            print(f"   Response: {response.json()}")
            test_results.append(True)
        else:
            print(f"❌ Expected 403, got {response.status_code}")
            test_results.append(False)
    except Exception as e:
        print(f"❌ Error: {e}")
        test_results.append(False)
    
    # Test 3: Analytics endpoint with wrong API key (should fail)
    print("\n3. Testing analytics endpoint with wrong API key...")
    try:
        response = requests.get(f"{base_url}/analytics?apiKey=wrongKey", timeout=10)
        if response.status_code == 403:
            print("✅ Analytics endpoint correctly rejected request with wrong API key")
            print(f"   Response: {response.json()}")
            test_results.append(True)
        else:
            print(f"❌ Expected 403, got {response.status_code}")
            test_results.append(False)
    except Exception as e:
        print(f"❌ Error: {e}")
        test_results.append(False)
    
    # Test 4: Analytics endpoint with correct API key (should succeed)
    print("\n4. Testing analytics endpoint with correct API key...")
    try:
        response = requests.get(f"{base_url}/analytics?apiKey=validKey", timeout=10)
        if response.status_code == 200:
            print("✅ Analytics endpoint correctly granted access with valid API key")
            print(f"   Response: {response.json()}")
            test_results.append(True)
        else:
            print(f"❌ Expected 200, got {response.status_code}")
            print(f"   Response body: {response.text}")
            test_results.append(False)
    except Exception as e:
        print(f"❌ Error: {e}")
        test_results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    
    if passed_tests == total_tests:
        print(f"🎉 All {total_tests} tests passed! Milestone 1 implementation is working correctly.")
        print("\nNote: Check the Flask app console for request logging output.")
        return 0
    else:
        print(f"❌ {passed_tests}/{total_tests} tests passed. Some issues need to be fixed.")
        return 1

if __name__ == "__main__":
    exit_code = test_milestone1()
    sys.exit(exit_code)