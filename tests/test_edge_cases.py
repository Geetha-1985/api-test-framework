import pytest
import allure

@allure.feature("Edge Cases & Boundary Tests")
class TestEdgeCases:
    """Edge cases and boundary test cases"""
    
    @allure.story("Empty Request Body")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_edge_001_empty_request_body(self, api_client, config, assertions):
        """TC_EDGE_001: Empty Request Body"""
        test_case = "TC_EDGE_001"
        
        # Make POST request with empty body
        url = f"{config.get_base_url('jsonplaceholder')}/posts"
        response = api_client.post(url, json_data={}, test_case=test_case)
        
        # JSONPlaceholder accepts empty bodies, but normally this would be 400
        # Adjust assertion based on actual API behavior
        assert response.status_code in [201, 400], \
            f"{test_case} - Unexpected status code: {response.status_code}"
    
    @allure.story("Maximum String Lengths")
    @allure.severity(allure.severity_level.MINOR)
    def test_tc_edge_002_maximum_string_lengths(self, api_client, config, 
                                              assertions, test_data_manager):
        """TC_EDGE_002: Maximum String Lengths"""
        test_case = "TC_EDGE_002"
        
        # Test with very long strings
        long_title = test_data_manager.generate_long_string(500)
        long_body = test_data_manager.generate_long_string(2000)
        
        post_data = {
            "title": long_title,
            "body": long_body,
            "userId": 1
        }
        
        url = f"{config.get_base_url('jsonplaceholder')}/posts"
        response = api_client.post(url, json_data=post_data, test_case=test_case)
        
        # JSONPlaceholder should accept this
        assertions.assert_status_code(response, 201, test_case)
        
        response_json = response.json()
        # Verify no truncation occurred
        assert len(response_json.get("title", "")) == len(long_title), \
            f"{test_case} - Title was truncated"
        assert len(response_json.get("body", "")) == len(long_body), \
            f"{test_case} - Body was truncated"
    
    @allure.story("Unicode and Special Characters")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_edge_003_unicode_special_characters(self, api_client, config, 
                                                  assertions, test_data_manager):
        """TC_EDGE_003: Unicode and Special Characters"""
        test_case = "TC_EDGE_003"
        
        unicode_data = test_data_manager.generate_unicode_data()
        post_data = {
            "title": unicode_data["name"],
            "body": f"Email: {unicode_data['email']} with special chars: 你好 🌟",
            "userId": 1
        }
        
        url = f"{config.get_base_url('jsonplaceholder')}/posts"
        response = api_client.post(url, json_data=post_data, test_case=test_case)
        
        assertions.assert_status_code(response, 201, test_case)
        
        response_json = response.json()
        # Verify unicode characters are preserved
        assert unicode_data["name"] in response_json.get("title", ""), \
            f"{test_case} - Unicode characters not preserved in title"