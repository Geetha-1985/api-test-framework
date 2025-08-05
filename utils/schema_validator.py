from jsonschema import validate, ValidationError
from typing import Dict, Any
import json

class SchemaValidator:
    """JSON Schema validation for API responses"""
    
    # Response schemas
    SCHEMAS = {
        'post': {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "body": {"type": "string"},
                "userId": {"type": "integer"}
            },
            "required": ["id", "title", "body", "userId"]
        },
        'user': {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "gender": {"type": "string", "enum": ["male", "female"]},
                "status": {"type": "string", "enum": ["active", "inactive"]}
            },
            "required": ["id", "name", "email", "gender", "status"]
        },
        'login_success': {
            "type": "object",
            "properties": {
                "token": {"type": "string", "minLength": 1}
            },
            "required": ["token"]
        },
        'error_response': {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            },
            "required": ["error"]
        },
        'validation_error': {
            "type": "object",
            "properties": {
                "field": {"type": "string"},
                "message": {"type": "string"}
            }
        }
    }
    
    def validate_response(self, response_data: Dict[str, Any], 
                         schema_name: str) -> tuple[bool, str]:
        """Validate response against schema"""
        try:
            schema = self.SCHEMAS.get(schema_name)
            if not schema:
                return False, f"Schema '{schema_name}' not found"
            
            validate(instance=response_data, schema=schema)
            return True, "Schema validation passed"
            
        except ValidationError as e:
            return False, f"Schema validation failed: {e.message}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def validate_response_list(self, response_data: list, 
                              item_schema_name: str) -> tuple[bool, str]:
        """Validate list response where each item follows a schema"""
        if not isinstance(response_data, list):
            return False, "Response is not a list"
        
        for index, item in enumerate(response_data):
            is_valid, error_msg = self.validate_response(item, item_schema_name)
            if not is_valid:
                return False, f"Item {index}: {error_msg}"
        
        return True, f"All {len(response_data)} items passed schema validation"