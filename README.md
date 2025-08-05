# API Automation Testing Framework Documentation

## Table of Contents
1. [Overview](#overview)
2. [Framework Architecture](#framework-architecture)
3. [Setup and Installation](#setup-and-installation)
4. [Configuration](#configuration)
5. [Running Tests](#running-tests)
6. [Test Structure](#test-structure)
7. [Features](#features)
8. [CI/CD Integration](#cicd-integration)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance](#maintenance)

## Overview

This API automation testing framework is built using Python and pytest, designed for comprehensive API testing with industry-standard practices. It provides automated testing for authentication, CRUD operations, data validation, error handling, performance testing, and edge cases.

### Key Features
- ✅ Configurable Environment Management
- ✅ Automatic Request/Response Logging
- ✅ Schema Validation for Responses
- ✅ Test Data Management and Cleanup
- ✅ Retry Mechanisms for Flaky Tests
- ✅ Parallel Test Execution Support
- ✅ Comprehensive Reporting with Logs
- ✅ CI/CD Pipeline Integration

### Supported APIs
- **JSONPlaceholder**: https://jsonplaceholder.typicode.com
- **ReqRes**: https://reqres.in/api
- **HTTPBin**: https://httpbin.org
- **GoRest**: https://gorest.co.in/public/v2

## Framework Architecture

```
api-test-framework/
├── config/
│   └── config.py                 # Environment configuration
├── utils/
│   ├── api_client.py            # HTTP client with retry logic
│   ├── logger.py                # Enhanced logging system
│   ├── schema_validator.py      # JSON schema validation
│   ├── test_data_manager.py     # Test data generation
│   └── assertions.py            # Custom assertion methods
├── tests/
│   ├── test_authentication.py   # Authentication tests
│   ├── test_crud_operations.py  # CRUD operation tests
│   ├── test_data_validation.py  # Data validation tests
│   ├── test_error_handling.py   # Error handling tests
│   ├── test_performance.py      # Performance tests
│   └── test_edge_cases.py       # Edge case tests
├── reports/                     # Test reports and logs
├── logs/                        # Application logs
├── conftest.py                  # Pytest configuration
├── pytest.ini                  # Pytest settings
├── requirements.txt             # Dependencies
├── Makefile                     # Build automation
├── docker-compose.yml           # Docker configuration
├── Dockerfile                   # Container definition
└── .github/workflows/           # CI/CD pipelines
```

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd api-test-framework
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   
   If the below error is seen, then execute the below steps.

   ![alt text](image.png)

   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process #Temporarily allow script execution (for current session only)
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser #Permanently allow scripts for your user

   venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment configuration**
   ```bash
   cp .env.txt .env
   ```

5. **Configure API tokens**
   - Edit `.env` file
   - Add your GoRest API token: `GOREST_TOKEN=your_token_here`

6. **Create necessary folders**
   -  mkdir logs
   -  mkdir reports 
   -  mkdir allure-results
 

## Configuration

### Environment Configuration

The framework supports multiple environments through the `config.py` file:

```python
ENVIRONMENTS = {
    'dev': { ... },
    'staging': { ... },
    'prod': { ... }
}
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TEST_ENV` | Target environment | `dev` |
| `GOREST_TOKEN` | GoRest API token | `""` |
| `REQUEST_TIMEOUT` | Request timeout in seconds | `30` |
| `RETRY_COUNT` | Number of retries for failed requests | `3` |
| `PARALLEL_WORKERS` | Number of parallel test workers | `4` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_REQUESTS` | Enable request/response logging | `true` |

### Test Configuration

Modify `pytest.ini` for test execution settings:

```ini
[tool:pytest]
addopts = --html=reports/report.html --allure-dir=reports/allure-results -v
markers = 
    smoke: Smoke tests for critical functionality
    regression: Full regression test suite
    performance: Performance and load tests
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest tests/

# Run with HTML report
pytest tests/ --html=reports/report.html

# Run with Allure reporting
pytest tests/ --alluredir=reports/allure-results
```

### Test Categories

```bash
# Smoke tests (critical functionality)
pytest tests/ -m smoke

# Regression tests (full suite)
pytest tests/ -m regression

# Performance tests
pytest tests/ -m performance

# Specific test file
pytest tests/test_authentication.py

# Specific test case
pytest tests/test_authentication.py::TestAuthentication::test_tc_auth_001_valid_authentication
```

### Parallel Execution

```bash
# Run with in parallel with specific number of workers
pytest tests/ -n 4
```

## Test Structure

### Test Case Naming Convention

Tests follow the pattern: `test_tc_<category>_<number>_<description>`

Example: `test_tc_auth_001_valid_authentication`

### Test Categories

1. **Authentication Tests** (`TC_AUTH_xxx`)
   - Valid authentication
   - Invalid credentials
   - Missing required fields

2. **CRUD Operations** (`TC_CRUD_xxx`)
   - Create resources
   - Read resources
   - Update resources
   - Delete resources

3. **Data Validation** (`TC_VALID_xxx`)
   - Missing required fields
   - Invalid data formats
   - Enum validation

4. **Error Handling** (`TC_ERROR_xxx`)
   - Resource not found (404)
   - Method not allowed (405)
   - Invalid endpoints

5. **Performance Tests** (`TC_PERF_xxx`)
   - Response time validation
   - Concurrent request handling
   - Pagination performance
   - Stress testing

6. **Edge Cases** (`TC_EDGE_xxx`)
   - Empty request bodies
   - Maximum string lengths
   - Unicode characters

### Test Data Management

The framework includes a comprehensive test data manager:

```python
# Generate user data
user_data = test_data_manager.generate_user_data(
    name="Custom Name",
    email="custom@email.com"
)

# Generate post data
post_data = test_data_manager.generate_post_data()

# Generate invalid data for negative testing
invalid_email = test_data_manager.generate_invalid_email()
long_string = test_data_manager.generate_long_string(1000)
unicode_data = test_data_manager.generate_unicode_data()
```

## Features

### 1. Configurable Environment Management

The framework supports multiple environments with easy switching:

```python
# Set environment via environment variable
export TEST_ENV=staging

# Or configure in .env file
TEST_ENV=prod
```

Each environment can have different:
- Base URLs
- Authentication tokens
- Timeout settings
- Retry configurations

### 2. Automatic Request/Response Logging

All API interactions are automatically logged with detailed information:

```python
# Request logging includes:
# - HTTP method and URL
# - Headers and authentication
# - Request body/payload
# - Test case identifier

# Response logging includes:
# - Status code
# - Response headers
# - Response body
# - Response time in milliseconds
```

Logs are saved to:
- Console output (formatted)
- Daily rotating log files in `logs/` directory
- Test reports (HTML/Allure)

### 3. Schema Validation for Responses

Automatic JSON schema validation ensures response structure consistency:

```python
# Define schemas for different response types
SCHEMAS = {
    'user': {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["id", "name", "email"]
    }
}

# Validate responses automatically
is_valid, message = schema_validator.validate_response(response_json, 'user')
```

### 4. Test Data Management and Cleanup

Comprehensive test data generation with cleanup tracking:

```python
# Generate realistic test data
user_data = test_data_manager.generate_user_data()

# Track created resources for cleanup
test_data_manager.track_created_resource("user", user_id, "gorest")

# Automatic cleanup after tests
cleanup_list = test_data_manager.get_cleanup_list()
```

### 5. Retry Mechanisms for Flaky Tests

Built-in retry logic for handling network issues and flaky tests:

```python
@retry(tries=3, delay=1, backoff=2)
def make_request(self, method, url, **kwargs):
    # Automatic retry with exponential backoff
    # Tries: 3 attempts
    # Delay: 1 second initial delay
    # Backoff: 2x multiplier (1s, 2s, 4s)
```

### 6. Parallel Test Execution Support

Run tests in parallel to reduce execution time:

```bash
# Auto-detect CPU cores
pytest tests/ -n auto

# Specify worker count
pytest tests/ -n 4

# Configure in pytest.ini
addopts = -n auto
```

### 7. Comprehensive Reporting with Logs

Multiple reporting formats supported:

#### HTML Reports
```bash
pytest tests/ --html=reports/report.html --self-contained-html
```

#### Allure Reports
```bash
pytest tests/ --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report
allure open reports/allure-report
```

#### JUnit XML Reports
```bash
pytest tests/ --junitxml=reports/junit.xml
```

### 8. CI/CD Pipeline Integration

Ready-to-use GitHub Actions workflow:

```yaml
# Automated test execution on:
# - Push to main/develop branches
# - Pull requests
# - Nightly schedule
# - Manual trigger

# Multiple Python versions: 3.8, 3.9, 3.10
# Test suites: smoke, regression, performance
# Artifact collection and reporting
```

```bash
.github/workflows/api-tests.yml
```

Features:
- **Multi-environment testing**: Different Python versions
- **Parallel execution**: Matrix strategy for test suites
- **Artifact collection**: Test reports and logs
- **Scheduled runs**: Nightly regression testing
- **Security scanning**: Dependency vulnerability checks


## Maintenance

### Adding New Tests

1. **Create test file** in `tests/` directory
2. **Follow naming convention**: `test_tc_<category>_<number>_<description>`
3. **Use fixtures** from `conftest.py`
4. **Add markers** for test categorization
5. **Update documentation**

Example new test:

```python
@allure.story("New Feature")
@pytest.mark.regression
def test_tc_new_001_feature_validation(self, api_client, config, assertions):
    """TC_NEW_001: New feature validation"""
    test_case = "TC_NEW_001"
    
    # Test implementation
    url = f"{config.get_base_url('service')}/endpoint"
    response = api_client.get(url, test_case=test_case)
    
    assertions.assert_status_code(response, 200, test_case)
```

### Adding New Schemas

Update `schema_validator.py`:

```python
SCHEMAS = {
    'new_schema': {
        "type": "object",
        "properties": {
            "field1": {"type": "string"},
            "field2": {"type": "integer"}
        },
        "required": ["field1", "field2"]
    }
}
```

### Updating Dependencies

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade pytest

# Update all packages
pip install --upgrade -r requirements.txt

# Update requirements.txt
pip freeze > requirements.txt
```

### Test Data Cleanup

For APIs that create persistent data:

```python
def cleanup_test_data(self, test_data_manager, api_client, config):
    """Clean up created test data"""
    cleanup_list = test_data_manager.get_cleanup_list()
    
    for resource in cleanup_list:
        if resource['service'] == 'gorest' and resource['type'] == 'user':
            url = f"{config.get_base_url('gorest')}/users/{resource['id']}"
            headers = config.get_headers('gorest')
            api_client.delete(url, headers=headers)
```


   
   
