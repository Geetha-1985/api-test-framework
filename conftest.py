import pytest
from config.config import Config
from utils.api_client import APIClient
from utils.logger import APILogger
from utils.schema_validator import SchemaValidator
from utils.test_data_manager import TestDataManager
from utils.assertions import APIAssertions

@pytest.fixture(scope="session")
def config():
    """Global configuration fixture"""
    return Config()

@pytest.fixture(scope="session")
def api_logger():
    """Global logger fixture"""
    return APILogger()

@pytest.fixture(scope="session")
def api_client(config, api_logger):
    """Global API client fixture"""
    return APIClient(config, api_logger)

@pytest.fixture(scope="session")
def schema_validator():
    """Schema validator fixture"""
    return SchemaValidator()

@pytest.fixture(scope="function")
def test_data_manager():
    """Test data manager fixture with cleanup"""
    manager = TestDataManager()
    yield manager
    # Cleanup logic would go here if needed
    manager.clear_cleanup_list()

@pytest.fixture(scope="session")
def assertions():
    """Custom assertions fixture"""
    return APIAssertions()

# addde after failure
@pytest.fixture(scope="session")
def gorest_token(config, request):
    """
    Fixture to fetch GoRest token from CLI option or config
    Priority: CLI token > .env/config
    """
    cli_token = request.config.getoption("--gorest-token")
    return cli_token or config.gorest_token


def pytest_addoption(parser):
    """Add custom CLI options to pytest"""
    parser.addoption("--gorest-token", action="store", default=None, help="GoRest API Token")

#till here

# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers"""
    for item in items:
        # Add smoke marker to critical tests
        if "auth" in item.name.lower() or "crud_001" in item.name:
            item.add_marker(pytest.mark.smoke)
        
        # Add performance marker to performance tests
        if "perf" in item.name.lower():
            item.add_marker(pytest.mark.performance)
        
        # Add regression marker to all tests by default
        item.add_marker(pytest.mark.regression)