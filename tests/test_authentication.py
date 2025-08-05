import pytest
import allure


@allure.feature("Authentication")
class TestAuthentication:
    """Authentication and Authorization test cases"""

    @allure.story("Valid Authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_tc_auth_001_valid_authentication(self, api_client, config,
                                               schema_validator, assertions):
        """TC_AUTH_001: Valid Authentication (ReqRes)"""
        test_case = "TC_AUTH_001"

        login_data = {
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }

        url = f"{config.get_base_url('reqres')}/login"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = api_client.post(url, json_data=login_data, headers=headers, test_case=test_case)

        # Assertions
        assertions.assert_status_code(response, 200, test_case)
        assertions.assert_response_time(response, 2000, test_case)

        response_json = response.json()
        assertions.assert_json_contains(response_json, ["token"], test_case)
        assertions.assert_non_empty_string(response_json, "token", test_case)

        # Optional: Schema validation
        is_valid, msg = schema_validator.validate_response(response_json, "login_success")
        assert is_valid, f"{test_case} - Schema validation failed: {msg}"

    @allure.story("Invalid Authentication")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_auth_002_invalid_credentials(self, api_client, config,
                                              schema_validator, assertions):
        """TC_AUTH_002: Invalid Credentials (ReqRes)"""
        test_case = "TC_AUTH_002"

        login_data = {
            "email": "eve.holt@reqres.in",
            "password": "wrongpassword"
        }

        url = f"{config.get_base_url('reqres')}/login"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = api_client.post(url, json_data=login_data, headers=headers, test_case=test_case)

        # Assertions
        assertions.assert_status_code(response, 400, test_case)
        assertions.assert_response_time(response, 2000, test_case)

        response_json = response.json()
        assertions.assert_json_contains(response_json, ["error"], test_case)
        assertions.assert_json_not_contains(response_json, ["token"], test_case)

        # Optional: Schema validation
        is_valid, msg = schema_validator.validate_response(response_json, "error_response")
        assert is_valid, f"{test_case} - Schema validation failed: {msg}"

    @allure.story("Missing Password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_auth_003_missing_password(self, api_client, config,
                                           assertions, schema_validator):
        """TC_AUTH_003: Missing Password (ReqRes)"""
        test_case = "TC_AUTH_003"

        login_data = {
            "email": "eve.holt@reqres.in"
        }

        url = f"{config.get_base_url('reqres')}/login"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = api_client.post(url, json_data=login_data, headers=headers, test_case=test_case)

        # Assertions
        assertions.assert_status_code(response, 400, test_case)
        assertions.assert_response_time(response, 2000, test_case)

        response_json = response.json()
        assertions.assert_json_contains(response_json, ["error"], test_case)
        assertions.assert_field_value(response_json, "error", "Missing password", test_case)

        # Optional: Schema validation
        is_valid, msg = schema_validator.validate_response(response_json, "error_response")
        assert is_valid, f"{test_case} - Schema validation failed: {msg}"
