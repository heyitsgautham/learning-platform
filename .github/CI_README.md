# CI/CD Setup

This repository includes a GitHub Actions workflow for continuous integration.

## CI Workflow (`ci.yml`)

The workflow automatically:

1. **Sets up the environment:**
   - Ubuntu latest runner
   - Python 3.11
   - PostgreSQL 15 service

2. **Installs dependencies:**
   - Caches pip dependencies for faster builds
   - Installs Python requirements

3. **Configures the database:**
   - Uses PostgreSQL service container
   - Waits for database to be ready
   - Tests database connection

4. **Runs the application:**
   - Sets up environment variables
   - Starts Flask app in background
   - Waits for app to be ready

5. **Executes tests:**
   - Runs the comprehensive test suite
   - Tests all middleware functionality
   - Validates API endpoints

## Triggered On

- **Push** to `main` or `develop` branches
- **Pull requests** to `main` branch

## Test Coverage

The CI workflow tests:

✅ **Global Middleware**: Request logging functionality  
✅ **Route-specific Middleware**: API key validation for `/analytics`  
✅ **Health Endpoint**: Basic application health check  
✅ **Analytics Protection**: Proper 403 responses for invalid/missing API keys  
✅ **Analytics Access**: Successful access with valid API key  

## Environment Variables

The CI uses these environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `ANALYTICS_API_KEY`: API key for analytics endpoint (set to "validKey")

## Local Testing

To run the same tests locally:

```bash
# Start PostgreSQL (Docker)
docker run --name learning-platform-db \
  -e POSTGRES_DB=learning_platform \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 -d postgres:15

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your database credentials

# Run the app
python app.py

# Run tests (in another terminal)
python test_milestone1.py
```