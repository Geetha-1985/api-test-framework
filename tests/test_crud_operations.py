import pytest
import allure


@allure.feature("CRUD Operations")
class TestCRUDOperations:
    """CRUD Operations test cases"""

    @allure.story("Create Resource")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_tc_crud_001_create_post_jsonplaceholder(self, api_client, config,
                                                     schema_validator, assertions,
                                                     test_data_manager):
        """TC_CRUD_001: Create Resource - JSONPlaceholder"""
        test_case = "TC_CRUD_001"

        # Test data
        post_data = test_data_manager.generate_post_data(
            title="Test Post Title",
            body="This is a test post body content for automation testing",
            userId=1
        )

        # Make request
        url = f"{config.get_base_url('jsonplaceholder')}/posts"
        response = api_client.post(url, json_data=post_data, test_case=test_case)

        # Assertions
        assertions.assert_status_code(response, 201, test_case)
        assertions.assert_response_time(response, 1000, test_case)

        response_json = response.json()
        assertions.assert_json_contains(response_json, ["id", "title", "body", "userId"], test_case)
        assertions.assert_field_value(response_json, "id", 101, test_case)  # JSONPlaceholder returns 101
        assertions.assert_field_value(response_json, "title", post_data["title"], test_case)
        assertions.assert_field_value(response_json, "body", post_data["body"], test_case)
        assertions.assert_field_value(response_json, "userId", post_data["userId"], test_case)

    @allure.story("Create User with Authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_crud_002_create_user_gorest(self, api_client, config,
                                            schema_validator, assertions,
                                            test_data_manager):
        """TC_CRUD_002: Create User - GoRest (Requires Token)"""
        test_case = "TC_CRUD_002"

        if not config.gorest_token:
            pytest.skip("GoRest token not configured")

        # Test data
        email = f"john.doe.automation+{test_data_manager.generate_random_string(6)}@example.com"
        user_data = test_data_manager.generate_user_data(
            name="John Doe Automation",
            email=email,
            gender="male",
            status="active"
        )

        # Make request
        url = f"{config.get_base_url('gorest')}/users"
        headers = config.get_headers('gorest')
        response = api_client.post(url, json_data=user_data, headers=headers, test_case=test_case)

        # Assertions
        assertions.assert_status_code(response, 201, test_case)

        response_json = response.json()
        assertions.assert_json_contains(response_json, ["id", "name", "email", "gender", "status"], test_case)

        # Track created resource for potential cleanup
        if "id" in response_json:
            test_data_manager.track_created_resource("user", response_json["id"], "gorest")

    @allure.story("Read Single Resource")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_crud_003_read_single_post(self, api_client, config,
                                          schema_validator, assertions):
        """TC_CRUD_003: Read Single Resource - JSONPlaceholder"""
        test_case = "TC_CRUD_003"

        # Make request
        url = f"{config.get_base_url('jsonplaceholder')}/posts/1"
        response = api_client.get(url, test_case=test_case)

        # Assertions
        assertions.assert_status_code(response, 200, test_case)

        response_json = response.json()
        assertions.assert_json_contains(response_json, ["id", "title", "body", "userId"], test_case)
        assertions.assert_field_type(response_json, "id", int, test_case)
        assertions.assert_field_type(response_json, "userId", int, test_case)
        assertions.assert_field_type(response_json, "title", str, test_case)
        assertions.assert_field_type(response_json, "body", str, test_case)

        # Schema validation
        is_valid, msg = schema_validator.validate_response(response_json, "post")
        assert is_valid, f"{test_case} - Schema validation failed: {msg}"
