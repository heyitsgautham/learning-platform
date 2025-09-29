# Smart Learning Platform

A comprehensive learning platform built with Flask and PostgreSQL, featuring role-based access control, OAuth2 authentication, and microservices architecture.

## Project Structure

```
learning-platform/
├── app.py                 # Main Flask application with middleware
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── routes/               # API route blueprints
│   ├── __init__.py
│   └── analytics.py      # Analytics routes with API key protection
├── models/               # Database models
│   ├── __init__.py
│   └── database.py       # Database configuration and initialization
└── services/             # Business logic services
    └── __init__.py
```

## Milestone 1 Features

### ✅ Backend Setup & Middleware

1. **Flask Project Structure**: Organized codebase with separate directories for routes, models, and services
2. **PostgreSQL Integration**: SQLAlchemy configuration with environment-based connection strings
3. **Global Middleware**: Logs every request with method, path, and timestamp
4. **Route-specific Middleware**: API key validation for `/analytics` endpoint
5. **Analytics Endpoint**: Protected route that requires `?apiKey=validKey` parameter

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL database

### Installation

1. **Clone and navigate to project**:
   ```bash
   cd learning-platform
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Configure PostgreSQL**:
   - Create a database named `learning_platform`
   - Update `DATABASE_URL` in `.env` with your credentials

5. **Run the application**:
   ```bash
   python app.py
   ```

## API Endpoints

### Health Check
- **GET** `/` - Returns API status and health information

### Analytics (Protected)
- **GET** `/analytics?apiKey=validKey` - Returns analytics access confirmation
- **Authentication**: Requires valid API key as query parameter
- **Response**: `{"message": "Analytics access granted"}`
- **Error**: Returns 403 if API key is missing or invalid

## Middleware Features

### Global Request Logging
Every incoming request is logged with:
- HTTP method (GET, POST, etc.)
- Request path
- Timestamp in ISO format

Example log output:
```
[2025-09-30T10:30:45.123456] GET /
[2025-09-30T10:30:50.789012] GET /analytics
```

### Analytics API Key Validation
The `/analytics` endpoint is protected by middleware that:
- Checks for `apiKey` query parameter
- Validates against `ANALYTICS_API_KEY` environment variable
- Returns 403 Forbidden if validation fails

## Testing

### Automated Testing (CI/CD)
This project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:
- Sets up PostgreSQL and Python environment
- Runs comprehensive tests on every push/PR
- Validates all middleware functionality

### Manual Testing
Run the test suite locally:
```bash
python test_milestone1.py
```

The test script validates:
- Health endpoint functionality
- Request logging middleware
- API key validation middleware
- Proper error responses (403 for invalid keys)
- Successful access with valid API key

## Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `FLASK_ENV`: Environment mode (development/production)
- `FLASK_DEBUG`: Enable debug mode (True/False)
- `ANALYTICS_API_KEY`: Valid API key for analytics endpoint (default: "validKey")

## Next Steps (Upcoming Milestones)

- **Milestone 2**: Async patterns & RBAC implementation
- **Milestone 3**: Microservices split (User + Course services)
- **Milestone 4**: REST API design with pagination, filtering, sorting
- **Milestone 5**: Swagger API documentation
- **Milestone 6**: Frontend dashboards
- **Milestone 7**: Docker containerization & GCP deployment

## Documentation

- **[CHANGELOG.md](CHANGELOG.md)** - Detailed project history and milestone progress
- **[CI Documentation](.github/CI_README.md)** - CI/CD setup and testing guide
- **[Project Instructions](.github/copilot-instructions.md)** - Complete project requirements