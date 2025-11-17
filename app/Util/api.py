import requests

class APIClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.token = token
    
    def request(self, method, endpoint, **kwargs):
        """Make API request with automatic token refresh"""
        headers = kwargs.pop('headers', {})
        
        # Add authorization header
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        
        # Make request
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=headers, **kwargs)
        
        # Check for new token
        new_token = response.headers.get('X-New-Token')
        if new_token:
            print('Token refreshed!')
            self.token = new_token
        
        return response
    
    def get(self, endpoint, **kwargs):
        return self.request('GET', endpoint, **kwargs)
    
    def post(self, endpoint, **kwargs):
        return self.request('POST', endpoint, **kwargs)

# Usage
client = APIClient('http://localhost:8000/api', token='your-token')

# Make request - token automatically refreshed
response = client.get('/user')
print(response.json())