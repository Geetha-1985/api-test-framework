from typing import Any, Dict, List
import time

class APIAssertions:
    """Custom assertions for API testing"""
    
    @staticmethod
    def assert_status_code(response, expected_code: int, test_case: str = None):
        """Assert response status code"""
        actual = response.status_code
        assert actual == expected_code, \
            f"Test: {test_case} - Expected status code {expected_code}, got {actual}"
    
    @staticmethod
    def assert_response_time(response, max_time_ms: int, test_case: str = None):
        """Assert response time is within limit"""
        actual_time = getattr(response, 'elapsed_ms', 
                             response.elapsed.total_seconds() * 1000)
        assert actual_time <= max_time_ms, \
            f"Test: {test_case} - Response time {actual_time}ms exceeds limit {max_time_ms}ms"
    
    @staticmethod
    def assert_json_contains(response_json: Dict, expected_fields: List[str], 
                           test_case: str = None):
        """Assert JSON response contains expected fields"""
        missing_fields = [field for field in expected_fields 
                         if field not in response_json]
        assert not missing_fields, \
            f"Test: {test_case} - Missing fields: {missing_fields}"
    
    @staticmethod
    def assert_json_not_contains(response_json: Dict, forbidden_fields: List[str], 
                               test_case: str = None):
        """Assert JSON response doesn't contain forbidden fields"""
        present_fields = [field for field in forbidden_fields 
                         if field in response_json]
        assert not present_fields, \
            f"Test: {test_case} - Forbidden fields present: {present_fields}"
    
    @staticmethod
    def assert_field_type(response_json: Dict, field: str, expected_type: type, 
                         test_case: str = None):
        """Assert field is of expected type"""
        if field in response_json:
            actual_type = type(response_json[field])
            assert actual_type == expected_type, \
                f"Test: {test_case} - Field '{field}' expected {expected_type.__name__}, got {actual_type.__name__}"
    
    @staticmethod
    def assert_field_value(response_json: Dict, field: str, expected_value: Any, 
                          test_case: str = None):
        """Assert field has expected value"""
        actual_value = response_json.get(field)
        assert actual_value == expected_value, \
            f"Test: {test_case} - Field '{field}' expected '{expected_value}', got '{actual_value}'"
    
    @staticmethod
    def assert_non_empty_string(response_json: Dict, field: str, test_case: str = None):
        """Assert field is non-empty string"""
        value = response_json.get(field)
        assert isinstance(value, str) and len(value) > 0, \
            f"Test: {test_case} - Field '{field}' should be non-empty string, got: {value}"