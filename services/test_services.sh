#!/bin/bash

# Microservices Test Script
echo "Testing Microservices..."

# Check if services are running
echo "Checking User Service (port 5002)..."
curl -s http://localhost:5002/ || echo "User Service not running on port 5002"

echo -e "\nChecking Course Service (port 5003)..."
curl -s http://localhost:5003/ || echo "Course Service not running on port 5003"

# Test User Service endpoints
echo -e "\n=== Testing User Service ==="
echo "Getting service info..."
curl -s http://localhost:5002/info | jq .

echo -e "\nGetting all users..."
curl -s http://localhost:5002/api/users | jq .

echo -e "\nGetting instructors..."
curl -s http://localhost:5002/api/users/instructors | jq .

# Test Course Service endpoints
echo -e "\n=== Testing Course Service ==="
echo "Getting service info..."
curl -s http://localhost:5003/info | jq .

echo -e "\nGetting all courses..."
curl -s http://localhost:5003/api/courses | jq .

echo -e "\nTesting pagination..."
curl -s "http://localhost:5003/api/courses?page=1&limit=2" | jq .

echo -e "\nTesting filtering..."
curl -s "http://localhost:5003/api/courses?category=tech" | jq .

echo -e "\nTesting sorting..."
curl -s "http://localhost:5003/api/courses?sort=title_desc" | jq .

echo -e "\n=== Testing Inter-Service Communication ==="
echo "Creating a test course (requires instructor_id from User Service)..."
curl -s -X POST http://localhost:5003/api/courses \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Course","instructor_id":1,"category":"test","description":"A test course"}' | jq .

echo -e "\nTest completed!"