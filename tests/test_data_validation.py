import pytest
import allure


@allure.feature("Data Validation")
class TestDataValidation:
    """Data validation test cases"""

    @allure.story("Missing Required Fields")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_valid_001_missing_required_fields(self, api_client, config, assertions, gorest_token):
        """TC_VALID_001: Missing Required Fields - GoRest"""
        test_case = "TC_VALID_001"

        if not gorest_token:
            pytest.skip("GoRest token not provided")

        # Test data - missing required email, gender, status fields
        user_data = {
            "name": "John Doe"
        }

        # Make request
        url = f"{config.get_base_url('gorest')}/users"
        headers = config.get_headers('gorest')
        response = api_client.post(url, json_data=user_data, headers=headers, test_case=test_case)

        # Assertions
        assertions.assert_status_code(response, 422, test_case)

        response_json = response.json()
        assert isinstance(response_json, list) or "field" in str(response_json), \
            f"{test_case} - Expected validation error format"

    @allure.story("Invalid Email Format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_valid_002_invalid_email_format(self, api_client, config, assertions, test_data_manager, gorest_token):
        """TC_VALID_002: Invalid Email Format - GoRest"""
        test_case = "TC_VALID_002"

        if not gorest_token:
            pytest.skip("GoRest token not provided")

        # Test data
        user_data = {
            "name": "John Doe",
            "email": test_data_manager.generate_invalid_email(),
            "gender": "male",
            "status": "active"
        }

        # Make request
        url = f"{config.get_base_url('gorest')}/users"
        headers = config.get_headers('gorest')
        response = api_client.post(url, json_data=user_data, headers=headers, test_case=test_case)

        # Assertions
        assertions.assert_status_code(response, 422, test_case)

        response_json = response.json()
        assert "email" in str(response_json).lower(), \
            f"{test_case} - Expected email validation error"

    @allure.story("Invalid Enum Values")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_valid_003_invalid_enum_values(self, api_client, config, assertions, gorest_token):
        """TC_VALID_003: Invalid Enum Values - GoRest"""
        test_case = "TC_VALID_003"

        if not gorest_token:
            pytest.skip("GoRest token not provided")

        # Test data with invalid enum values
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "gender": "unknown",
            "status": "maybe"
        }

        # Make request
        url = f"{config.get_base_url('gorest')}/users"
        headers = config.get_headers('gorest')
        response = api_client.post(url, json_data=user_data, headers=headers, test_case=test_case)

        # Assertions
        assertions.assert_status_code(response, 422, test_case)

        response_json = response.json()
        response_str = str(response_json).lower()
        assert "gender" in response_str or "status" in response_str, \
            f"{test_case} - Expected gender/status validation error"
