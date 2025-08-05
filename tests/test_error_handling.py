import pytest
import allure

@allure.feature("Error Handling")
class TestErrorHandling:
    """Error handling test cases"""
    
    @allure.story("Resource Not Found")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_error_001_resource_not_found(self, api_client, config, assertions):
        """TC_ERROR_001: Resource Not Found - JSONPlaceholder"""
        test_case = "TC_ERROR_001"
        
        # Make request to non-existent resource
        url = f"{config.get_base_url('jsonplaceholder')}/posts/99999"
        response = api_client.get(url, test_case=test_case)
        
        # Assertions
        assertions.assert_status_code(response, 404, test_case)
        
        response_json = response.json()
        assert response_json == {}, f"{test_case} - Expected empty response body"
    
    @allure.story("Method Not Allowed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_error_002_method_not_allowed(self, api_client, config, assertions):
        """TC_ERROR_002: Method Not Allowed - HTTPBin"""
        test_case = "TC_ERROR_002"
        
        # Make DELETE request to GET endpoint
        url = f"{config.get_base_url('httpbin')}/get"
        response = api_client.delete(url, test_case=test_case)
        
        # Assertions
        assertions.assert_status_code(response, 405, test_case)
    
    @allure.story("Invalid URL Path")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_error_003_invalid_url_path(self, api_client, config, assertions):
        """TC_ERROR_003: Invalid URL Path - JSONPlaceholder"""
        test_case = "TC_ERROR_003"
        
        # Make request to invalid endpoint
        url = f"{config.get_base_url('jsonplaceholder')}/invalid-endpoint"
        response = api_client.get(url, test_case=test_case)
        
        # Assertions
        assertions.assert_status_code(response, 404, test_case)
        
        response_json = response.json()
        assert response_json == {}, f"{test_case} - Expected empty response body"