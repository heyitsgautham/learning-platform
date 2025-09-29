# Microservices Setup Guide

## Services Overview

This application is split into two microservices:

1. **User Service** (Port 5002) - Manages users, authentication, and roles
2. **Course Service** (Port 5003) - Manages courses and enrollments

## Database Configuration

Both services connect to the same PostgreSQL database using the `DATABASE_URL` environment variable.

## Environment Variables

Create a `.env` file in each service directory with:

```
DATABASE_URL=postgresql://username:password@localhost:5432/learning_platform
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
USER_SERVICE_URL=http://localhost:5002
```

## Running the Services

### User Service (Port 5002)
```bash
cd services/user_service
pip install -r requirements.txt
python app.py
```

### Course Service (Port 5003)
```bash
cd services/course_service
pip install -r requirements.txt
python app.py
```

## Service Endpoints

### User Service (http://localhost:5002)
- `GET /` - Health check
- `GET /info` - Service information
- `POST /auth/login` - Google OAuth login
- `POST /auth/logout` - Logout
- `GET /auth/profile` - Get current user profile
- `POST /auth/change-role` - Change user role
- `GET /api/users` - Get all users
- `GET /api/users/{id}` - Get specific user
- `GET /api/users/by-role/{role}` - Get users by role
- `PUT /api/users/{id}/role` - Update user role
- `GET /api/users/instructors` - Get all instructors

### Course Service (http://localhost:5003)
- `GET /` - Health check
- `GET /info` - Service information
- `GET /api/courses` - Get courses (with pagination, filtering, sorting)
- `POST /api/courses` - Create new course
- `GET /api/courses/{id}` - Get specific course
- `PUT /api/courses/{id}` - Update course
- `DELETE /api/courses/{id}` - Delete course
- `POST /api/courses/{id}/enroll` - Enroll student in course
- `GET /api/enrollments/student/{id}` - Get student enrollments

## Inter-Service Communication

The Course Service automatically calls the User Service to:
- Fetch instructor details when returning course data
- Verify instructor existence when creating courses
- Enrich course responses with instructor information

## Testing

Use the provided test scripts or tools like Postman to test the endpoints.
Make sure both services are running before testing inter-service communication.