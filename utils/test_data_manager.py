from faker import Faker
from typing import Dict, Any, List
import random
import string

class TestDataManager:
    """Test data generation and management"""
    
    def __init__(self):
        self.fake = Faker()
        self.created_resources = []  # Track created resources for cleanup
    
    def generate_user_data(self, **overrides) -> Dict[str, Any]:
        """Generate test user data"""
        data = {
            "name": self.fake.name(),
            "email": self.fake.unique.email(),
            "gender": random.choice(["male", "female"]),
            "status": random.choice(["active", "inactive"])
        }
        data.update(overrides)
        return data
    
    def generate_post_data(self, **overrides) -> Dict[str, Any]:
        """Generate test post data"""
        data = {
            "title": self.fake.sentence(nb_words=4),
            "body": self.fake.paragraph(nb_sentences=3),
            "userId": random.randint(1, 10)
        }
        data.update(overrides)
        return data
    
    def generate_invalid_email(self) -> str:
        """Generate invalid email for negative testing"""
        invalid_formats = [
            "invalid-email",
            "user@",
            "@domain.com",
            "user.domain.com",
            "user@domain"
        ]
        return random.choice(invalid_formats)
    
    def generate_long_string(self, length: int = 1000) -> str:
        """Generate long string for boundary testing"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def generate_unicode_data(self) -> Dict[str, str]:
        """Generate data with unicode characters"""
        return {
            "name": "José María González-Pérez £$%^",
            "email": "josé@müller.com"
        }
    
    def track_created_resource(self, resource_type: str, resource_id: Any, 
                              service: str = None):
        """Track created resources for cleanup"""
        self.created_resources.append({
            "type": resource_type,
            "id": resource_id,
            "service": service
        })
    
    def get_cleanup_list(self) -> List[Dict]:
        """Get list of resources to cleanup"""
        return self.created_resources.copy()
    
    def clear_cleanup_list(self):
        """Clear the cleanup list"""
        self.created_resources.clear()

    def generate_random_string(self, length=6):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))