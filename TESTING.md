# GIVC Core Academy - Testing Guide

## Test Coverage Summary

Current test coverage: **74%**

## Backend Testing

### Running Tests

```bash
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::test_register_user -v
```

### Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py          # Pytest configuration and fixtures
└── test_auth.py         # Authentication tests
```

### Current Test Coverage by Module

| Module | Coverage |
|--------|----------|
| app/models/* | 100% |
| app/schemas/* | 100% |
| app/config.py | 100% |
| app/main.py | 96% |
| app/api/v1/auth.py | 66% |
| app/api/v1/courses.py | 67% |
| app/core/security.py | 62% |
| **Overall** | **74%** |

### Existing Tests

#### Authentication Tests (`test_auth.py`)

1. ✅ `test_register_user` - User registration flow
2. ✅ `test_register_duplicate_email` - Duplicate email validation
3. ✅ `test_login_success` - Successful login
4. ✅ `test_login_invalid_credentials` - Invalid credentials handling
5. ✅ `test_health_check` - Health check endpoint

### Adding New Tests

Example test structure:

```python
def test_example(client):
    """Test description"""
    response = client.post(
        "/api/v1/endpoint",
        json={"key": "value"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "expected_value"
```

## Frontend Testing

### Setup

```bash
cd frontend

# Install test dependencies
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
```

### Running Tests

```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

## Integration Testing

### API Integration Tests

Test complete user flows:

1. **User Registration and Login Flow**
   ```bash
   # Register
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "testpass123", "full_name": "Test User", "preferred_language": "ar"}'
   
   # Login
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=test@example.com&password=testpass123"
   ```

2. **Course Enrollment Flow**
   ```bash
   # Get token from login
   TOKEN="your-access-token"
   
   # List courses
   curl http://localhost:8000/api/v1/courses
   
   # Enroll in course
   curl -X POST http://localhost:8000/api/v1/enrollments \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"course_id": 1, "subscription_tier": "standard", "modality": "virtual_live"}'
   ```

3. **Assessment Flow**
   ```bash
   # Get course assessments
   curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/assessments/course/1
   
   # Start assessment
   curl -X POST -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/assessments/1/start
   ```

## Manual Testing Checklist

### Backend API

- [ ] User Registration
  - [ ] Valid registration
  - [ ] Duplicate email validation
  - [ ] Invalid Saudi National ID
  - [ ] Password requirements

- [ ] User Login
  - [ ] Valid credentials
  - [ ] Invalid credentials
  - [ ] Token generation
  - [ ] Token refresh

- [ ] Courses
  - [ ] List courses
  - [ ] Get course details
  - [ ] Filter by course type

- [ ] Enrollments
  - [ ] Create enrollment
  - [ ] List my enrollments
  - [ ] View enrollment progress

- [ ] Assessments
  - [ ] List course assessments
  - [ ] Start assessment
  - [ ] View results

- [ ] Payments
  - [ ] Create payment intent
  - [ ] List my payments

### Frontend

- [ ] Homepage
  - [ ] Arabic RTL layout
  - [ ] English LTR layout
  - [ ] Responsive design

- [ ] Authentication
  - [ ] Registration form
  - [ ] Login form
  - [ ] Token persistence

- [ ] Course Catalog
  - [ ] Course listing
  - [ ] Course details
  - [ ] Enrollment button

### Mobile App

- [ ] App launches successfully
- [ ] Navigation works
- [ ] API integration
- [ ] Offline handling

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test registration endpoint
ab -n 100 -c 10 -p register.json -T application/json \
  http://localhost:8000/api/v1/auth/register

# Test health check
ab -n 1000 -c 100 http://localhost:8000/health
```

### Expected Performance Targets

- Health check: < 50ms response time
- Registration: < 200ms response time
- Login: < 150ms response time
- Course listing: < 100ms response time

## Security Testing

### Automated Security Checks

```bash
# CodeQL analysis (already passing with 0 alerts)
# Run as part of CI/CD pipeline
```

### Manual Security Tests

- [ ] SQL Injection attempts (SQLAlchemy protects)
- [ ] XSS attempts (React auto-escaping protects)
- [ ] CSRF tokens for state-changing operations
- [ ] JWT token expiration
- [ ] MFA enforcement for admin roles
- [ ] Rate limiting on authentication endpoints

## Continuous Integration

### GitHub Actions Workflow (Example)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node
        uses: actions/setup-node@v2
        with:
          node-version: 20
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm test
```

## Test Data

### Sample Test Users

Created by `backend/scripts/seed_data.py`:

1. **Admin User**
   - Email: admin@givc.sa
   - Password: admin123
   - Type: ADMIN

2. **Student User**
   - Email: student@example.com
   - Password: student123
   - Type: STUDENT
   - National ID: 1234567890

### Sample Course

- Title: Clinical Coding Professional - KSA
- Code: CCP-KSA-001
- Type: CCP_KSA
- Covers: ICD-10-AM, SBS, AR-DRG

## Troubleshooting Tests

### Tests Fail with Database Errors

```bash
# Clean test database
rm -f backend/test.db

# Run tests again
cd backend && pytest
```

### Import Errors

```bash
# Ensure you're in the right directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Tests Fail

```bash
# Clear cache
cd frontend
rm -rf node_modules .next
npm install
```

## Coverage Goals

Target: **>80% code coverage**

Current: **74%**

### Areas to Improve Coverage

1. Services (0% coverage)
   - adaptive_learning.py
   - analytics_service.py
   - payment_service.py

2. API Endpoints (48-67% coverage)
   - Add tests for error cases
   - Test authorization/permissions
   - Test validation

3. Dependencies (41% coverage)
   - Test authentication middleware
   - Test role-based access control

## Test Best Practices

1. **Isolation**: Each test should be independent
2. **Fixtures**: Use pytest fixtures for common setup
3. **Mocking**: Mock external services (Stripe, email)
4. **Assertions**: Clear, specific assertions
5. **Documentation**: Document what each test validates
6. **Coverage**: Aim for >80% coverage
7. **Performance**: Keep tests fast (<1s each)

## Next Steps

1. Add more API endpoint tests
2. Add service layer tests
3. Add frontend component tests
4. Set up CI/CD pipeline
5. Add end-to-end tests with Playwright
