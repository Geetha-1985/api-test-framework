import pytest
import allure
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

@allure.feature("Performance")
class TestPerformance:
    """Performance test cases"""
    
    @allure.story("Response Time Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.performance
    def test_tc_perf_001_response_time_validation(self, api_client, config, 
                                                assertions, test_data_manager):
        """TC_PERF_001: Response Time Validation - JSONPlaceholder"""
        test_case = "TC_PERF_001"
        base_url = config.get_base_url('jsonplaceholder')
        
        # Test GET single post (< 500ms)
        response = api_client.get(f"{base_url}/posts/1", test_case=f"{test_case}_single")
        assertions.assert_status_code(response, 200, f"{test_case}_single")
        assertions.assert_response_time(response, 500, f"{test_case}_single")
        
        # Test GET all posts (< 1 second)
        response = api_client.get(f"{base_url}/posts", test_case=f"{test_case}_collection")
        assertions.assert_status_code(response, 200, f"{test_case}_collection")
        assertions.assert_response_time(response, 1000, f"{test_case}_collection")
        
        # Test POST request (< 1 second)
        post_data = test_data_manager.generate_post_data()
        response = api_client.post(f"{base_url}/posts", json_data=post_data, 
                                 test_case=f"{test_case}_post")
        assertions.assert_status_code(response, 201, f"{test_case}_post")
        assertions.assert_response_time(response, 1000, f"{test_case}_post")
    
    @allure.story("Concurrent Request Handling")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_tc_perf_002_concurrent_request_handling(self, api_client, config, assertions):
        """TC_PERF_002: Concurrent Request Handling - HTTPBin"""
        test_case = "TC_PERF_002"
        url = f"{config.get_base_url('httpbin')}/delay/1"
        
        def make_request():
            start_time = time.time()
            response = api_client.get(url, test_case=test_case)
            end_time = time.time()
            return response, end_time - start_time
        
        # Execute 10 concurrent requests
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in as_completed(futures)]
        total_time = time.time() - start_time
        
        # Assertions
        assert len(results) == 10, f"{test_case} - Expected 10 responses"
        
        # All requests should succeed
        for response, request_time in results:
            assertions.assert_status_code(response, 200, test_case)
        
        # Total time should be around 1 second (not 10 seconds)
        assert total_time < 3, f"{test_case} - Concurrent requests took too long: {total_time}s"
    
    @allure.story("Pagination Performance")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_tc_perf_003_pagination_performance(self, api_client, config, assertions):
        """TC_PERF_003: Pagination Performance - JSONPlaceholder"""
        test_case = "TC_PERF_003"
        base_url = config.get_base_url('jsonplaceholder')
        
        pages_to_test = [1, 2, 5]
        response_times = []
        
        for page in pages_to_test:
            url = f"{base_url}/posts?_page={page}&_limit=20"
            response = api_client.get(url, test_case=f"{test_case}_page_{page}")
            
            assertions.assert_status_code(response, 200, f"{test_case}_page_{page}")
            
            response_time = getattr(response, 'elapsed_ms', 
                                  response.elapsed.total_seconds() * 1000)
            response_times.append(response_time)
        
        # Check that response times are consistent (no significant degradation)
        max_time = max(response_times)
        min_time = min(response_times)
        
        # Allow up to 50% variation between pages
        assert max_time <= min_time * 1.5, \
            f"{test_case} - Performance degradation detected. Times: {response_times}"
    
    @allure.story("Stress Test")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    def test_tc_perf_004_stress_test(self, api_client, config, assertions, test_data_manager):
        """TC_PERF_004: Stress Test - HTTPBin Echo"""
        test_case = "TC_PERF_004"
        url = f"{config.get_base_url('httpbin')}/post"
        
        # Generate 1KB test payload
        payload = {
            "data": test_data_manager.generate_long_string(1000),
            "timestamp": time.time()
        }
        
        successful_requests = 0
        failed_requests = 0
        response_times = []
        
        def make_stress_request():
            nonlocal successful_requests, failed_requests
            try:
                start_time = time.time()
                response = api_client.post(url, json_data=payload, test_case=test_case)
                end_time = time.time()
                
                if response.status_code == 200:
                    successful_requests += 1
                    response_times.append((end_time - start_time) * 1000)
                else:
                    failed_requests += 1
            except Exception:
                failed_requests += 1
        
        # Execute 50 requests over 30 seconds
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for i in range(50):
                futures.append(executor.submit(make_stress_request))
                if i < 49:  # Don't sleep after last request
                    time.sleep(0.6)  # Spread requests over 30 seconds
            
            # Wait for all requests to complete
            for future in as_completed(futures):
                future.result()
        
        total_time = time.time() - start_time
        
        # Assertions
        total_requests = successful_requests + failed_requests
        success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
        
        assert success_rate >= 95, \
            f"{test_case} - Success rate {success_rate}% below 95% threshold"
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            assert avg_response_time <= 5000, \
                f"{test_case} - Average response time {avg_response_time}ms too high"