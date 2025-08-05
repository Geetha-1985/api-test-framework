import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management for different environments"""
    
    ENVIRONMENTS = {
        'dev': {
            'jsonplaceholder': 'https://jsonplaceholder.typicode.com',
            'reqres': 'https://reqres.in/api',
            'httpbin': 'https://httpbin.org',
            'gorest': 'https://gorest.co.in/public/v2'
        },
        'staging': {
            'jsonplaceholder': 'https://jsonplaceholder.typicode.com',
            'reqres': 'https://reqres.in/api',
            'httpbin': 'https://httpbin.org',
            'gorest': 'https://gorest.co.in/public/v2'
        },
        'prod': {
            'jsonplaceholder': 'https://jsonplaceholder.typicode.com',
            'reqres': 'https://reqres.in/api',
            'httpbin': 'https://httpbin.org',
            'gorest': 'https://gorest.co.in/public/v2'
        }
    }
    
    def __init__(self, environment: str = None):
        self.environment = environment or os.getenv('TEST_ENV', 'dev')
        self.base_urls = self.ENVIRONMENTS.get(self.environment, self.ENVIRONMENTS['dev'])
        
        # API Tokens
        self.gorest_token = os.getenv('GOREST_TOKEN', '')
        
        # Test Configuration
        self.timeout = int(os.getenv('REQUEST_TIMEOUT', '30'))
        self.retry_count = int(os.getenv('RETRY_COUNT', '3'))
        self.parallel_workers = int(os.getenv('PARALLEL_WORKERS', '4'))
        
        # Logging Configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_requests = os.getenv('LOG_REQUESTS', 'true').lower() == 'true'
        
    def get_base_url(self, service: str) -> str:
        """Get base URL for a specific service"""
        return self.base_urls.get(service, '')

    def get_headers(self, service: str = None) -> Dict[str, str]:
        """Get default headers for requests"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Only add Authorization header for gorest
        if service and service.lower() == 'gorest':
            token = self.gorest_token
            if token:
                headers['Authorization'] = f'Bearer {token}'

        return headers