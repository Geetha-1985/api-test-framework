import json
from typing import Any, Dict
from loguru import logger
import sys

class APILogger:
    """Enhanced logging for API requests and responses"""
    
    def __init__(self):
        # Configure loguru
        logger.remove()
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO"
        )
        logger.add(
            "logs/test_execution_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation="1 day",
            retention="7 days"
        )
    
    def log_request(self, method: str, url: str, headers: Dict = None, 
                   body: Any = None, test_case: str = None):
        """Log API request details"""
        log_data = {
            "type": "REQUEST",
            "test_case": test_case,
            "method": method,
            "url": url,
            "headers": headers or {},
            "body": body
        }
        logger.info(f"API Request: {json.dumps(log_data, indent=2)}")
    
    def log_response(self, response, test_case: str = None):
        """Log API response details"""
        try:
            response_body = response.json() if response.text else {}
        except:
            response_body = response.text
            
        log_data = {
            "type": "RESPONSE",
            "test_case": test_case,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response_body,
            "response_time_ms": round(response.elapsed.total_seconds() * 1000, 2)
        }
        logger.info(f"API Response: {json.dumps(log_data, indent=2)}")
    
    def log_error(self, error: Exception, test_case: str = None):
        """Log errors"""
        logger.error(f"Test Case: {test_case} - Error: {str(error)}")
    
    def log_validation(self, validation_type: str, result: bool, 
                      details: str = None, test_case: str = None):
        """Log validation results"""
        status = "PASSED" if result else "FAILED"
        message = f"Validation [{validation_type}] - {status}"
        if details:
            message += f" - {details}"
        if test_case:
            message = f"Test Case: {test_case} - {message}"
        
        if result:
            logger.success(message)
        else:
            logger.error(message)