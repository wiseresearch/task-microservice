# test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test that the health endpoint returns a valid response."""
    response = client.get('/health')
    assert response.status_code in [200, 503] # Depending on Redis connection in CI
    assert b"status" in response.data