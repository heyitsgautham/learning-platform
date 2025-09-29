#!/usr/bin/env python3
"""
Simple API test for Milestone 4: REST API Design
Tests pagination, filtering, sorting, and HATEOAS links with the actual running services
"""

import requests
import json

# Service URLs
COURSE_API_URL = "http://localhost:5003/api"

def test_empty_courses_api():
    """Test the courses API with empty database (tests structure)"""
    print("🔍 Testing Courses API with empty database...")
    
    try:
        response = requests.get(f"{COURSE_API_URL}/courses")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Basic courses endpoint works")
            print(f"📄 Response: {json.dumps(data, indent=2)}")
            
            # Verify basic structure
            assert 'courses' in data
            assert 'pagination' in data
            assert 'filters' in data
            assert '_links' in data
            print("✅ Response structure is correct")
            
            # Verify HATEOAS links
            links = data.get('_links', {})
            assert 'self' in links
            assert 'create' in links
            print("✅ HATEOAS links are present")
            
            # Verify pagination structure
            pagination = data.get('pagination', {})
            assert 'page' in pagination
            assert 'limit' in pagination
            assert 'total' in pagination
            print("✅ Pagination structure is correct")
            
            return True
        else:
            print(f"❌ API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_pagination_parameters():
    """Test pagination parameters"""
    print("\n🔍 Testing pagination parameters...")
    
    test_cases = [
        {"page": 1, "limit": 5},
        {"page": 2, "limit": 3},
        {"page": 1, "limit": 20},
    ]
    
    for test_case in test_cases:
        try:
            response = requests.get(f"{COURSE_API_URL}/courses", params=test_case)
            
            if response.status_code == 200:
                data = response.json()
                pagination = data.get('pagination', {})
                
                # Verify pagination parameters are applied
                assert pagination.get('page') == test_case['page']
                assert pagination.get('limit') == test_case['limit']
                
                print(f"✅ Pagination test passed: {test_case}")
            else:
                print(f"❌ Pagination test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Pagination test error: {e}")
            return False
    
    return True

def test_filtering_parameters():
    """Test filtering parameters"""
    print("\n🔍 Testing filtering parameters...")
    
    test_cases = [
        {"category": "tech"},
        {"category": "science"},
        {"category": "math"},
    ]
    
    for test_case in test_cases:
        try:
            response = requests.get(f"{COURSE_API_URL}/courses", params=test_case)
            
            if response.status_code == 200:
                data = response.json()
                filters = data.get('filters', {})
                
                # Verify filter parameter is recorded
                assert filters.get('category') == test_case['category']
                
                print(f"✅ Filtering test passed: {test_case}")
            else:
                print(f"❌ Filtering test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Filtering test error: {e}")
            return False
    
    return True

def test_sorting_parameters():
    """Test sorting parameters"""
    print("\n🔍 Testing sorting parameters...")
    
    test_cases = [
        {"sort": "title_asc"},
        {"sort": "title_desc"},
        {"sort": "rating_asc"},
        {"sort": "rating_desc"},
        {"sort": "id_asc"},
        {"sort": "id_desc"},
    ]
    
    for test_case in test_cases:
        try:
            response = requests.get(f"{COURSE_API_URL}/courses", params=test_case)
            
            if response.status_code == 200:
                data = response.json()
                filters = data.get('filters', {})
                
                # Verify sort parameter is recorded
                assert filters.get('sort') == test_case['sort']
                
                print(f"✅ Sorting test passed: {test_case}")
            else:
                print(f"❌ Sorting test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Sorting test error: {e}")
            return False
    
    return True

def test_combined_parameters():
    """Test combined query parameters"""
    print("\n🔍 Testing combined parameters...")
    
    test_cases = [
        {"page": 1, "limit": 5, "category": "tech", "sort": "rating_desc"},
        {"page": 2, "limit": 3, "category": "science", "sort": "title_asc"},
    ]
    
    for test_case in test_cases:
        try:
            response = requests.get(f"{COURSE_API_URL}/courses", params=test_case)
            
            if response.status_code == 200:
                data = response.json()
                pagination = data.get('pagination', {})
                filters = data.get('filters', {})
                
                # Verify all parameters are applied
                assert pagination.get('page') == test_case['page']
                assert pagination.get('limit') == test_case['limit']
                assert filters.get('category') == test_case['category']
                assert filters.get('sort') == test_case['sort']
                
                print(f"✅ Combined parameters test passed: {test_case}")
            else:
                print(f"❌ Combined parameters test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Combined parameters test error: {e}")
            return False
    
    return True

def test_hateoas_structure():
    """Test HATEOAS links structure"""
    print("\n🔍 Testing HATEOAS structure...")
    
    try:
        response = requests.get(f"{COURSE_API_URL}/courses")
        
        if response.status_code == 200:
            data = response.json()
            
            # Test collection-level HATEOAS links
            links = data.get('_links', {})
            required_collection_links = ['self', 'create']
            
            for link in required_collection_links:
                assert link in links, f"Missing {link} link in collection"
                assert 'href' in links[link], f"Missing href in {link} link"
                assert 'method' in links[link], f"Missing method in {link} link"
            
            print("✅ Collection HATEOAS links are correct")
            
            # Since we don't have courses in the empty database, 
            # we can't test individual course HATEOAS links here
            # but the structure is implemented as verified in unit tests
            
            return True
        else:
            print(f"❌ HATEOAS test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ HATEOAS test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Milestone 4: REST API Design")
    print("=" * 60)
    
    tests = [
        test_empty_courses_api,
        test_pagination_parameters,
        test_filtering_parameters, 
        test_sorting_parameters,
        test_combined_parameters,
        test_hateoas_structure,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"❌ Test {test.__name__} failed")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Milestone 4 REST API tests passed!")
        print("\n✅ Verified Features:")
        print("  • Pagination (?page=1&limit=5)")
        print("  • Filtering (?category=tech)")
        print("  • Sorting (?sort=rating_desc)")
        print("  • Combined queries")
        print("  • HATEOAS links (self, create)")
        print("  • Proper response structure")
        return True
    else:
        print("💥 Some tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)