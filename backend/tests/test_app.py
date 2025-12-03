import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client

def test_status_endpoint(client):
    """Test the /api/status endpoint"""
    rv = client.get('/api/status')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'ok'

def test_health_endpoint(client):
    """Test the /health endpoint"""
    rv = client.get('/health')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'healthy'