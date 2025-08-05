import requests
import time
from typing import Dict, Any, Optional
from retry import retry
from utils.logger import APILogger

class APIClient:
    """Enhanced API client with logging and retry mechanisms"""

    def __init__(self, config, logger: APILogger = None):
        self.config = config
        self.logger = logger or APILogger()

    @retry(tries=3, delay=1, backoff=2)
    def make_request(self, method: str, url: str, headers: Dict = None,
                     json_data: Any = None, params: Dict = None,
                     test_case: str = None, timeout: int = None) -> requests.Response:
        """Make HTTP request with retry mechanism and logging"""

        # Use headers as provided — DO NOT merge with session headers
        request_headers = headers if headers is not None else {}
        request_timeout = timeout or self.config.timeout

        # Log request
        if self.config.log_requests:
            self.logger.log_request(method, url, request_headers, json_data, test_case)

        try:
            start_time = time.time()
            response = requests.request(  # Use raw requests to avoid session injections
                method=method,
                url=url,
                headers=request_headers,
                json=json_data,
                params=params,
                timeout=request_timeout
            )
            end_time = time.time()

            response.elapsed_ms = round((end_time - start_time) * 1000, 2)

            # Log response
            if self.config.log_requests:
                self.logger.log_response(response, test_case)

            return response

        except Exception as e:
            self.logger.log_error(e, test_case)
            raise

    def get(self, url: str, headers: Dict = None, params: Dict = None,
            test_case: str = None, **kwargs) -> requests.Response:
        """GET request wrapper"""
        return self.make_request('GET', url, headers=headers, params=params,
                                 test_case=test_case, **kwargs)

    def post(self, url: str, json_data: Any = None, headers: Dict = None,
             test_case: str = None, **kwargs) -> requests.Response:
        """POST request wrapper"""
        return self.make_request('POST', url, headers=headers, json_data=json_data,
                                 test_case=test_case, **kwargs)

    def put(self, url: str, json_data: Any = None, headers: Dict = None,
            test_case: str = None, **kwargs) -> requests.Response:
        """PUT request wrapper"""
        return self.make_request('PUT', url, headers=headers, json_data=json_data,
                                 test_case=test_case, **kwargs)

    def delete(self, url: str, headers: Dict = None, test_case: str = None,
               **kwargs) -> requests.Response:
        """DELETE request wrapper"""
        return self.make_request('DELETE', url, headers=headers,
                                 test_case=test_case, **kwargs)
