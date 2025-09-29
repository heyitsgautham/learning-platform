# CHANGELOG

All notable changes to the Smart Learning Platform project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.4.0] - 2025-09-30 - Milestone 4: REST API Design

### Added

#### 🔍 **Advanced Query Parameters**
- **Pagination**: `GET /courses?page=1&limit=5`
  - Configurable page size and page number
  - Comprehensive pagination metadata (total, pages, has_next, has_prev)
  - Default values: page=1, limit=10
- **Filtering**: `GET /courses?category=tech`
  - Category-based course filtering
  - Extensible filtering system for future filters
- **Sorting**: `GET /courses?sort=rating_desc`
  - Multiple sort options: title_asc, title_desc, rating_asc, rating_desc, id_asc, id_desc
  - Default sorting by id_asc
- **Combined Queries**: `GET /courses?page=1&limit=5&category=tech&sort=rating_desc`
  - All query parameters work together seamlessly

#### 🔗 **HATEOAS (Hypermedia as the Engine of Application State)**
- **Course Resources**: Each course response includes navigational links
  - `self`: Link to get the specific course
  - `update`: Link to update the course (PUT)
  - `delete`: Link to delete the course (DELETE)
  - `enroll`: Link to enroll in the course (POST)
  - `instructor`: Link to instructor details in User Service
- **Collection Resources**: Course list responses include collection links
  - `self`: Link to current page with all applied filters
  - `create`: Link to create new courses
  - `next`: Link to next page (when available)
  - `prev`: Link to previous page (when available)
- **Enrollment Resources**: Enrollment responses include related links
  - `self`: Link to student enrollments
  - `course`: Link to the enrolled course
  - `student`: Link to student details in User Service

#### 🌐 **REST Best Practices**
- **HTTP Verbs**: Proper use of GET, POST, PUT, DELETE
- **Resource-Based URLs**: Clear, hierarchical URL structure
- **Consistent Response Formats**: Standardized JSON responses
- **Error Handling**: Appropriate HTTP status codes (200, 201, 400, 404)
- **Content Negotiation**: JSON content-type handling

#### 📊 **Enhanced API Responses**
- **Enriched Course Data**: Instructor details fetched from User Service
- **Pagination Metadata**: Complete pagination information in responses
- **Filter Context**: Current filter and sort parameters in responses
- **Link Relations**: Self-descriptive API with discoverable actions

### Changed
- Course Service API now fully supports pagination, filtering, and sorting
- All course-related endpoints now include HATEOAS links
- Enhanced response structures with metadata and navigation

### Technical Details
- **Pagination**: SQLAlchemy pagination with configurable limits
- **Filtering**: Dynamic query building with category filters
- **Sorting**: Database-level ordering for performance
- **HATEOAS**: Dynamic link generation based on request context
- **Inter-Service**: Course Service calls User Service for instructor data enrichment

## [0.3.0] - 2025-09-30 - Milestone 3: Microservices Split

### Added

#### 🏗️ Microservices Architecture
- **User Service**: Standalone Flask app for user management, authentication, and roles
- **Course Service**: Standalone Flask app for course and enrollment management
- **Independent Flask apps**: Each service has its own models, routes, and requirements
- **Docker support**: Dockerfiles for each service and a Docker Compose file for local orchestration

#### 🔗 Inter-Service Communication
- **Course Service calls User Service** to fetch instructor details for course data
- **HTTP-based service discovery** using environment variable `USER_SERVICE_URL`
- **Instructor validation**: Course creation verifies instructor existence via User Service

#### 🗄️ Shared Database
- Both services connect to the same PostgreSQL database (`learning_platform`)
- Shared schema for users, courses, and enrollments

#### 🧪 Testing & Documentation
- Comprehensive test suite for microservices structure and integration
- Service README and test scripts for local verification

### Changed
- Refactored monolithic codebase into two microservices with clear separation of concerns

### Removed
- Monolithic course/user management from main app (now in microservices)

## [0.2.0] - 2025-09-30 - Milestone 2: Async Patterns & RBAC

### Added

#### 🔄 **Async Patterns Implementation**
- **Async Report Generation**: `GET /generateReport` endpoint
  - Simulates long-running task with `asyncio.sleep(3)` for 3-second processing delay
  - Non-blocking async implementation prevents request queue blocking
  - Returns JSON response: `{"status": "Report generated", "timestamp": "2025-09-30T..."}`
  - Proper async/await pattern with asyncio event loop management
  - Thread-safe execution using `asyncio.new_event_loop()` and `loop.run_until_complete()`

#### 🔐 **OAuth2 Authentication with Google**
- **Complete OAuth2 Flow**: Google-only authentication implementation
  - Login initiation: `GET /auth/login` - Redirects to Google OAuth consent screen
  - Callback handling: `GET /auth/callback` - Processes Google OAuth response
  - User profile access: `GET /auth/profile` - Returns authenticated user information
  - Logout functionality: `POST /auth/logout` - Clears user session
- **Google OAuth Configuration**: 
  - Client ID and Client Secret environment variable support
  - Proper OAuth scopes: `openid email profile`
  - Secure redirect URI handling for localhost development
  - Graceful degradation when OAuth credentials are not configured
- **Session Management**: 
  - Flask session-based user state management
  - Secure session configuration with HTTP-only cookies
  - User context persistence across requests

#### 👥 **User Management System**
- **User Database Model**: Complete User entity with role-based fields
  ```python
  class User(db.Model):
      id = Primary key
      email = Unique email address
      google_id = Google OAuth identifier
      name = Full user name
      role = Enum('student', 'teacher', 'admin')
      created_at/updated_at = Timestamp tracking
  ```
- **Role Assignment**: Default 'student' role for new users
- **Admin Role Management**: `PUT /auth/users/<id>/role` endpoint for role updates (admin-only)
- **User Profile API**: JSON serialization with `to_dict()` method

#### 🛡️ **Role-Based Access Control (RBAC)**
- **RBAC Middleware System**: Comprehensive decorator-based access control
  - `@require_auth`: Basic authentication requirement
  - `@require_role(role)`: Specific single role requirement
  - `@require_roles([roles])`: Multiple role options support
  - `get_current_user()`: Helper function for user context access
- **Protected Route Examples**: Demonstration of RBAC in action
  - **Student Routes**: Course viewing and enrollment (`/api/courses`, `/api/courses/<id>/enroll`)
  - **Teacher Routes**: Course creation and management (`POST /api/courses`, `PUT /api/courses/<id>`)
  - **Admin Routes**: Analytics access and user management (`/admin/analytics`, role updates)
- **Proper HTTP Status Codes**: 401 Unauthorized, 403 Forbidden responses
- **Detailed Error Messages**: Clear role requirement communication

#### 🎓 **Course Management API (Demo Implementation)**
- **Course CRUD Operations**: RESTful course management endpoints
  - `GET /api/courses` - List all courses (students, teachers, admins)
  - `POST /api/courses` - Create new course (teachers, admins only)
  - `PUT /api/courses/<id>` - Update course (teachers, admins only)
  - `POST /api/courses/<id>/enroll` - Enroll in course (students only)
- **Sample Data Structure**: Course entities with id, title, instructor, category
- **Role-Based Access**: Different permissions per user role
- **Admin Analytics**: `GET /admin/analytics` - Course statistics (admins only)

### Enhanced

#### 🔧 **Application Configuration**
- **OAuth Environment Variables**: 
  ```bash
  GOOGLE_CLIENT_ID=your-google-client-id
  GOOGLE_CLIENT_SECRET=your-google-client-secret
  SECRET_KEY=your-session-secret-key
  ```
- **Session Security**: HTTP-only cookies, secure session management
- **Development Mode**: OAuth credential validation with graceful fallbacks

#### 🧪 **Testing Infrastructure**
- **Milestone 2 Test Suite**: `test_milestone2.py` with comprehensive async and RBAC testing
  - **Health Check Validation**: Basic application health verification
  - **Async Pattern Testing**: `/generateReport` endpoint timing validation (3+ second delay)
  - **Middleware Testing**: Analytics API key protection verification
  - **OAuth Route Testing**: Authentication flow endpoint availability
  - **RBAC Testing**: Protected route access control validation
- **All Tests Passing**: 5/5 test scenarios successfully validated
- **Integration Testing**: Real HTTP requests to running Flask application

#### 📦 **Dependency Management**
- **New Dependencies Added**:
  - `asyncio==3.4.3` - Async pattern support
  - `Authlib==1.2.1` - OAuth2 client implementation
  - `Flask-Session==0.5.0` - Session management
  - `pytest` - Testing framework enhancement

### Technical Implementation Details

#### 🔄 **Async Architecture**
```python
@app.route('/generateReport', methods=['GET'])
def generate_report():
    async def process_report():
        await asyncio.sleep(3)  # Simulate processing
        return {"status": "Report generated", "timestamp": datetime.now().isoformat()}
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(process_report())
        return jsonify(result)
    finally:
        loop.close()
```

#### 🔐 **OAuth2 Configuration for Google Cloud Console**
**Authorized JavaScript Origins:**
```
http://localhost:5001
http://127.0.0.1:5001
```

**Authorized Redirect URIs:**
```
http://localhost:5001/auth/callback
http://127.0.0.1:5001/auth/callback
```

#### 🛡️ **RBAC Implementation Pattern**
```python
@courses_bp.route('/courses', methods=['POST'])
@require_roles(['teacher', 'admin'])
def create_course():
    current_user = get_current_user()
    # Course creation logic with proper role validation
```

#### 🗄️ **Database Schema Updates**
- **Users Table**: Added with proper constraints and indexes
- **Role Enumeration**: PostgreSQL enum type for role validation
- **Timestamp Tracking**: Created/updated timestamp automation
- **Unique Constraints**: Email and Google ID uniqueness enforcement

### 📁 **Project Structure Updates**

```
learning-platform/
├── app.py                      # Enhanced with OAuth and session config
├── requirements.txt            # Updated with async and OAuth dependencies
├── test_milestone2.py         # New comprehensive test suite
├── routes/
│   ├── auth.py                # NEW: Complete OAuth2 implementation
│   ├── courses.py             # NEW: RBAC-protected course management
│   └── analytics.py           # Existing analytics endpoint
├── models/
│   └── database.py            # Enhanced with User model
├── middleware/
│   ├── __init__.py            # NEW: Middleware package
│   └── rbac.py                # NEW: Role-based access control decorators
└── .env.example               # Updated with OAuth configuration
```

### 🚦 **API Endpoints Summary**

#### 🔓 **Public Endpoints**
- `GET /` - Health check
- `GET /generateReport` - Async report generation (3s delay)

#### 🔐 **Authentication Endpoints**
- `GET /auth/login` - Initiate Google OAuth flow
- `GET /auth/callback` - Handle OAuth callback
- `GET /auth/profile` - Get current user profile (auth required)
- `POST /auth/logout` - Clear user session

#### 👥 **Role-Protected Endpoints**
- `GET /api/courses` - List courses (student, teacher, admin)
- `POST /api/courses` - Create course (teacher, admin)
- `PUT /api/courses/<id>` - Update course (teacher, admin)
- `POST /api/courses/<id>/enroll` - Enroll in course (student only)
- `GET /admin/analytics` - View analytics (admin only)
- `PUT /auth/users/<id>/role` - Update user role (admin only)

#### 🛡️ **Protected Endpoints**
- `GET /analytics?apiKey=validKey` - Analytics with API key middleware

### 🧪 **Test Results**
```
============================================================
MILESTONE 2 TESTS: Async Patterns & RBAC
============================================================
✅ Health check working correctly
✅ /generateReport route working correctly (3.01 seconds)
✅ Analytics endpoint correctly blocks/accepts API key
✅ Login route exists and responds appropriately
✅ Profile route correctly requires authentication
✅ Courses route correctly requires authentication
✅ Create course route correctly requires authentication
============================================================
TEST RESULTS: 5/5 tests passed
🎉 All Milestone 2 tests passed!
============================================================
```

### 🔒 **Security Features**

#### 🛡️ **Authentication Security**
- **OAuth2 State Management**: Secure state parameter handling
- **Session Security**: HTTP-only cookies, secure session configuration
- **Token Validation**: Proper OAuth token verification
- **User Context**: Secure user session management

#### 🔐 **Authorization Security**
- **Role-Based Access**: Granular permission control
- **Endpoint Protection**: Decorator-based access control
- **Error Handling**: Secure error messages without information leakage
- **Session Validation**: Active user session verification

#### 🌐 **API Security**
- **CORS Considerations**: Prepared for cross-origin resource sharing
- **Input Validation**: JSON request validation
- **HTTP Status Codes**: Proper security status code usage (401, 403)

### ⚠️ **Known Limitations & Next Steps**

#### 🔧 **Current Limitations**
- **Single OAuth Provider**: Google-only authentication (by design)
- **In-Memory Session Store**: Flask session storage (suitable for development)
- **Sample Data**: Course data stored in memory (database implementation pending)
- **Development Server**: Flask development server usage

#### 🎯 **Milestone 3 Preparation**
- **Microservices Architecture**: Ready for service separation
- **Service Communication**: Foundation for inter-service calls
- **Database Models**: Extensible for course and enrollment entities
- **API Patterns**: Established patterns for service-to-service communication

### 💡 **Development Notes**

#### 🔄 **Async Pattern Benefits**
- **Non-Blocking Execution**: Prevents request queue blocking during long operations
- **Scalability**: Foundation for high-concurrency request handling
- **Performance**: Efficient resource utilization for I/O-bound operations

#### 🛡️ **RBAC Pattern Benefits**
- **Decorator Pattern**: Clean, reusable access control
- **Role Flexibility**: Easy addition of new roles and permissions
- **Maintenance**: Centralized authorization logic
- **Testing**: Isolated testable access control components

---

This milestone successfully implements comprehensive async patterns and robust role-based access control, establishing a secure and scalable foundation for the microservices architecture planned in Milestone 3.

## [0.1.0] - 2025-09-30 - Milestone 1: Backend Setup & Middleware

### Added

#### 🏗️ **Project Foundation**
- **Flask Application Structure**: Organized project with separate directories for routes, models, and services
- **PostgreSQL Integration**: SQLAlchemy configuration with environment-based connection strings
- **Environment Configuration**: `.env` file support with database credentials and API keys
- **Dependencies Management**: Complete `requirements.txt` with all necessary packages

#### 🔧 **Middleware Implementation**
- **Global Request Logging Middleware**: Logs every HTTP request with method, path, and ISO timestamp
  - Format: `[2025-09-30T10:30:45.123456] GET /analytics`
  - Applied to all routes automatically
- **Route-Specific API Key Validation**: Protected `/analytics` endpoint with middleware
  - Validates `apiKey=validKey` query parameter
  - Returns 403 Forbidden for missing or invalid API keys
  - Environment configurable via `ANALYTICS_API_KEY`

#### 🌐 **API Endpoints**
- **Health Check**: `GET /` - Returns application status and health information
- **Analytics Endpoint**: `GET /analytics?apiKey=validKey` - Protected analytics access
  - Middleware-protected route
  - Proper error handling for authentication failures

#### 🗄️ **Database Setup**
- **SQLAlchemy Configuration**: Modern SQLAlchemy 2.0+ with proper connection handling
- **Database Initialization**: Automatic table creation with retry logic
- **PostgreSQL Support**: Full PostgreSQL integration with Docker container setup
- **Connection Resilience**: Retry mechanism for database connectivity during startup

#### 🧪 **Testing Infrastructure**
- **Comprehensive Test Suite**: `test_milestone1.py` with 4 test scenarios
  - Health endpoint validation
  - API key middleware testing (missing, invalid, valid scenarios)
  - Timeout and error handling
  - Exit code support for CI/CD integration
- **Manual Testing Support**: Docker-based PostgreSQL setup instructions

#### 🚀 **CI/CD Pipeline**
- **GitHub Actions Workflow**: `.github/workflows/ci.yml`
  - Automated PostgreSQL service setup
  - Python 3.11 environment configuration
  - Dependency caching for performance
  - Background Flask app execution
  - Comprehensive endpoint testing
  - Health checks and cleanup procedures
- **CI Documentation**: Detailed setup and usage instructions
- **Status Badge**: GitHub Actions status badge in README

#### 📚 **Documentation**
- **Comprehensive README**: Setup instructions, API documentation, feature overview
- **CI Documentation**: Separate CI/CD setup and testing guide
- **Environment Template**: `.env.example` with all required configuration variables
- **Project Structure**: Clear directory organization and file descriptions

### Technical Details

#### 🔧 **Configuration**
```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/learning_platform

# Application
FLASK_ENV=development
FLASK_DEBUG=True
ANALYTICS_API_KEY=validKey
```

#### 📁 **Project Structure**
```
learning-platform/
├── app.py                    # Main Flask application with middleware
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── test_milestone1.py       # Comprehensive test suite
├── routes/                  # API route blueprints
│   ├── __init__.py
│   └── analytics.py         # Protected analytics endpoint
├── models/                  # Database models and configuration
│   ├── __init__.py
│   └── database.py          # SQLAlchemy setup with retry logic
├── services/                # Business logic services (prepared for future)
│   └── __init__.py
└── .github/
    ├── workflows/
    │   └── ci.yml          # GitHub Actions CI pipeline
    └── CI_README.md        # CI/CD documentation
```

#### 🐳 **Docker Setup**
```bash
# PostgreSQL Container
docker run --name learning-platform-db \
  -e POSTGRES_DB=learning_platform \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 -d postgres:15
```

#### 🚦 **Application Ports**
- **Flask Application**: Port 5001 (changed from 5000 due to macOS ControlCenter conflict)
- **PostgreSQL**: Port 5432

### Infrastructure Notes

#### 🔄 **Database Connection Handling**
- Retry mechanism with 10 attempts and 2-second delays
- Graceful error handling for connection failures
- Automatic table creation on successful connection
- SQLAlchemy 2.0+ compatibility with proper connection context

#### 🛡️ **Security Considerations**
- API key validation through environment variables
- Database credentials externalized to environment
- Proper HTTP status codes for unauthorized access
- Request logging for security monitoring

#### 🧪 **Testing Approach**
- Integration testing with real PostgreSQL database
- Middleware functionality validation
- Error scenario testing (403 responses)
- CI/CD automation for continuous validation

### Known Issues and Limitations

#### ⚠️ **Current Limitations**
- **Development Server**: Using Flask development server (not production-ready)
- **Local PostgreSQL Conflict**: Requires stopping local PostgreSQL services
- **Single API Key**: Only supports one analytics API key (environment-based)
- **No Authentication**: Basic API key protection only (OAuth2 coming in Milestone 2)

#### 🔧 **Environment Dependencies**
- **Docker Required**: For PostgreSQL container setup
- **Python 3.11+**: Specific Python version requirement
- **Port Availability**: Requires ports 5001 and 5432 to be available

### Migration Notes for Future Milestones

#### 🎯 **Milestone 2 Preparation**
- Database models ready for user and role tables
- Service layer structure prepared for business logic
- Blueprint pattern established for new route modules
- Environment configuration extensible for OAuth2 credentials

#### 🔄 **Upgrade Considerations**
- **Production WSGI Server**: Consider Gunicorn or uWSGI for production deployment
- **Database Migrations**: Implement proper migration scripts with Flask-Migrate
- **Logging Enhancement**: Consider structured logging with proper log levels
- **Configuration Management**: Consider configuration classes for different environments

### Dependencies

#### 📦 **Core Dependencies**
- `Flask==2.3.3` - Web framework
- `SQLAlchemy==2.0.23` - Database ORM
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `python-dotenv==1.0.0` - Environment variable management
- `Flask-Migrate==4.0.5` - Database migrations
- `requests==2.31.0` - HTTP testing library

#### 🧪 **Development Tools**
- Comprehensive test suite with requests library
- Docker for database containerization
- GitHub Actions for CI/CD
- Environment template for easy setup

---

### 📝 **Development Notes**

This milestone successfully establishes the foundation for the Smart Learning Platform with:
- ✅ Robust middleware architecture
- ✅ Database integration and connection handling
- ✅ Comprehensive testing and CI/CD
- ✅ Clear project structure and documentation
- ✅ Production-ready patterns and practices

The implementation follows Flask best practices and establishes patterns that will scale well for the remaining milestones, particularly the upcoming OAuth2 integration and RBAC implementation in Milestone 2.