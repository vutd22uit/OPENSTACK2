"""
API endpoint tests
"""
import pytest
from app import create_app

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_health_check(self, client):
        """Test health endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'

    def test_readiness_check(self, client):
        """Test readiness endpoint"""
        response = client.get('/ready')
        assert response.status_code == 200
        assert response.json['status'] == 'ready'

class TestAPIEndpoints:
    """Test API endpoints"""

    def test_get_status(self, client):
        """Test status endpoint"""
        response = client.get('/api/v1/status')
        assert response.status_code == 200
        assert response.json['status'] == 'operational'

    def test_get_data_pagination(self, client):
        """Test data pagination"""
        response = client.get('/api/v1/data?page=1&limit=10')
        assert response.status_code == 200
        assert 'data' in response.json
        assert 'page' in response.json
        assert 'limit' in response.json

    def test_get_data_invalid_pagination(self, client):
        """Test invalid pagination parameters"""
        response = client.get('/api/v1/data?page=-1&limit=1000')
        assert response.status_code == 400

    def test_create_data_valid(self, client):
        """Test creating data with valid input"""
        data = {
            'name': 'Test Item',
            'description': 'Test description'
        }
        response = client.post('/api/v1/data',
                               json=data,
                               content_type='application/json')
        assert response.status_code == 201
        assert response.json['name'] == 'Test Item'

    def test_create_data_missing_fields(self, client):
        """Test creating data with missing fields"""
        data = {'name': 'Test'}
        response = client.post('/api/v1/data',
                               json=data,
                               content_type='application/json')
        assert response.status_code == 400

    def test_create_data_xss_prevention(self, client):
        """Test XSS prevention in input"""
        data = {
            'name': '<script>alert("xss")</script>',
            'description': 'Test'
        }
        response = client.post('/api/v1/data',
                               json=data,
                               content_type='application/json')
        assert response.status_code == 201
        # Should be sanitized
        assert '<script>' not in response.json['name']

    def test_get_data_by_id_not_found(self, client):
        """Test getting non-existent data"""
        response = client.get('/api/v1/data/99999')
        assert response.status_code == 404

class TestSecurityHeaders:
    """Test security headers"""

    def test_security_headers_present(self, client):
        """Test that security headers are set"""
        response = client.get('/health')
        headers = response.headers

        assert 'X-Content-Type-Options' in headers
        assert headers['X-Content-Type-Options'] == 'nosniff'

        assert 'X-Frame-Options' in headers
        assert headers['X-Frame-Options'] == 'DENY'

        assert 'X-XSS-Protection' in headers
        assert 'Strict-Transport-Security' in headers
        assert 'Content-Security-Policy' in headers
