"""Utility functions and classes for API testing"""

import requests
from typing import Dict, Any, Optional, Union, List
from test_config import BASE_URL, TIMEOUT

def format_test_name(name: str) -> str:
    """Format test name for display by:
    1. Removing 'test_' prefix
    2. Replacing underscores with spaces
    3. Converting to title case
    4. Ensuring 'ID' stays uppercase
    """
    name = name.replace("test_", "").replace("_", " ").title()
    return name.replace("Id", "ID")

class APIClient:
    """Generic API client for making HTTP requests"""
    
    def __init__(self, base_url: str = BASE_URL, timeout: int = TIMEOUT):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def _make_request(self, method: str, endpoint: str, expected_status: int = None, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs['timeout'] = self.timeout
        
        # Don't fail on status code if we're expecting a specific error status
        if expected_status is not None and expected_status >= 400:
            kwargs['allow_redirects'] = True
        
        try:
            response = requests.request(method, url, **kwargs)
            return response
        except requests.RequestException as e:
            raise AssertionError(f"Request failed: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, 
            expected_status: int = None) -> requests.Response:
        """Make GET request"""
        return self._make_request('GET', endpoint, expected_status=expected_status, 
                                 params=params, headers=headers)

    def post(self, endpoint: str, json: Dict[str, Any], headers: Optional[Dict] = None, 
            expected_status: int = None) -> requests.Response:
        """Make POST request"""
        return self._make_request('POST', endpoint, expected_status=expected_status, 
                                 json=json, headers=headers)

    def put(self, endpoint: str, json: Dict[str, Any], headers: Optional[Dict] = None,
           expected_status: int = None) -> requests.Response:
        """Make PUT request"""
        return self._make_request('PUT', endpoint, expected_status=expected_status,
                                 json=json, headers=headers)

    def delete(self, endpoint: str, headers: Optional[Dict] = None,
              expected_status: int = None) -> requests.Response:
        """Make DELETE request"""
        return self._make_request('DELETE', endpoint, expected_status=expected_status,
                                 headers=headers)

class TestAssertions:
    """Common test assertions for API responses"""
    
    @staticmethod
    def assert_status_code(response: requests.Response, expected_code: int):
        """Assert response status code"""
        assert response.status_code == expected_code, \
            f"Expected status code {expected_code}, got {response.status_code}"

    @staticmethod
    def assert_json_field(response: requests.Response, field: str, expected_value: Any = None):
        """Assert JSON response field value or just existence if expected_value is None"""
        data = response.json()
        assert field in data, f"Field '{field}' not found in response"
        if expected_value is not None:
            assert data[field] == expected_value, \
                f"Expected {field}='{expected_value}', got '{data[field]}'"

    @staticmethod
    def assert_json_fields_present(response: requests.Response, fields: list):
        """Assert JSON response contains required fields"""
        data = response.json()
        for field in fields:
            assert field in data, f"Required field '{field}' not found in response"

    @staticmethod
    def assert_sorted_by_field(response: requests.Response, field: str, reverse: bool = False):
        """Assert JSON response array is sorted by field"""
        data = response.json()
        values = [item[field] for item in data]
        assert values == sorted(values, reverse=reverse), \
            f"Response not sorted by '{field}'"
            
    @staticmethod
    def assert_json_type(response: requests.Response, expected_type: Union[type, List[type]]):
        """Assert JSON response has expected type"""
        data = response.json()
        if isinstance(expected_type, list):
            assert isinstance(data, list), f"Expected a list, got {type(data).__name__}"
        else:
            assert isinstance(data, expected_type), \
                f"Expected {expected_type.__name__}, got {type(data).__name__}"