import requests
import time
import sys

# Configuration
BASE_URL = "http://localhost:8080"  # Nginx reverse proxy
API_ENDPOINT = "/api/status"
HEALTH_ENDPOINT = "/health"
STATIC_FILE = "/"  # Index page

def test_api_status():
    """Test the /api/status endpoint"""
    print("Testing /api/status endpoint...")
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}{API_ENDPOINT}")
        end_time = time.time()
        
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                print(f"✓ API status endpoint test PASSED (Latency: {latency:.2f} ms)")
                return True, latency
            else:
                print("✗ API status endpoint test FAILED - Unexpected response")
                return False, latency
        else:
            print(f"✗ API status endpoint test FAILED - Status code: {response.status_code}")
            return False, latency
    except Exception as e:
        print(f"✗ API status endpoint test FAILED - Exception: {e}")
        return False, 0

def test_health_endpoint():
    """Test the /health endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}{HEALTH_ENDPOINT}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                print("✓ Health endpoint test PASSED")
                return True
            else:
                print("✗ Health endpoint test FAILED - Unexpected response")
                return False
        else:
            print(f"✗ Health endpoint test FAILED - Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health endpoint test FAILED - Exception: {e}")
        return False

def test_static_file():
    """Test static file availability"""
    print("Testing static file availability...")
    try:
        response = requests.get(f"{BASE_URL}{STATIC_FILE}")
        
        if response.status_code == 200:
            if '<title>DevOps Sample App</title>' in response.text:
                print("✓ Static file availability test PASSED")
                return True
            else:
                print("✗ Static file availability test FAILED - Unexpected content")
                return False
        else:
            print(f"✗ Static file availability test FAILED - Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Static file availability test FAILED - Exception: {e}")
        return False

def test_latency(latency):
    """Test if latency is acceptable (< 1 second)"""
    print("Testing latency...")
    if latency < 1000:  # Less than 1 second (1000 ms)
        print("✓ Latency test PASSED")
        return True
    else:
        print(f"✗ Latency test FAILED - Latency: {latency:.2f} ms")
        return False

def main():
    """Main test function"""
    print("Starting API tests...\n")
    
    # Test API status endpoint
    status_passed, latency = test_api_status()
    
    # Test health endpoint
    health_passed = test_health_endpoint()
    
    # Test static file availability
    static_passed = test_static_file()
    
    # Test latency
    latency_passed = test_latency(latency)
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"API Status Endpoint: {'PASSED' if status_passed else 'FAILED'}")
    print(f"Health Endpoint: {'PASSED' if health_passed else 'FAILED'}")
    print(f"Static File Availability: {'PASSED' if static_passed else 'FAILED'}")
    print(f"Latency Test (< 1s): {'PASSED' if latency_passed else 'FAILED'}")
    
    # Overall result
    all_passed = status_passed and health_passed and static_passed and latency_passed
    
    print("\n" + "="*50)
    if all_passed:
        print("ALL TESTS PASSED! ✓")
        return 0
    else:
        print("SOME TESTS FAILED! ✗")
        return 1

if __name__ == "__main__":
    sys.exit(main())