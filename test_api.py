"""
Test script for Image Analysis API
Tests all endpoints with various scenarios
"""

import requests
import json
import os
from pathlib import Path

# Configuration
API_URL = "http://localhost:8000"
API_KEY = "test-api-key-12345"
HEADERS = {"X-API-Key": API_KEY}

def print_section(title):
    """Print test section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_result(test_name, status, details=""):
    """Print test result"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {test_name}")
    if details:
        print(f"   Details: {details}")

def test_health_check():
    """Test 1: Health check endpoint"""
    print_section("TEST 1: Health Check - GET /")
    try:
        response = requests.get(f"{API_URL}/", headers=HEADERS)
        print_result("Server Health", response.status_code == 200, f"Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print_result("Server Health", False, str(e))
        return False

def test_health_endpoint():
    """Test 2: Health status endpoint"""
    print_section("TEST 2: Health Status - GET /health")
    try:
        response = requests.get(f"{API_URL}/health", headers=HEADERS)
        print_result("Health Endpoint", response.status_code == 200, f"Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print_result("Health Endpoint", False, str(e))
        return False

def test_upload_without_api_key():
    """Test 3: Upload without API key (should fail)"""
    print_section("TEST 3: Upload Without API Key (Expected: 422 or 401)")
    try:
        # Create a temporary image file
        from PIL import Image
        import io
        
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
        response = requests.post(f"{API_URL}/api/upload", files=files)  # No API key
        
        is_success = response.status_code in [401, 422]
        print_result("API Key Required", is_success, f"Status: {response.status_code}")
        if response.status_code in [401, 422]:
            print(f"   Error: {response.json().get('detail', 'API key required')}")
        return is_success
    except Exception as e:
        print_result("API Key Required", False, str(e))
        return False

def test_upload_invalid_file_type():
    """Test 4: Upload invalid file type"""
    print_section("TEST 4: Upload Invalid File Type (Expected: 400)")
    try:
        # Create a temporary text file
        test_file = Path("test.txt")
        test_file.write_text("This is not an image")
        
        with open(test_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_URL}/api/upload", headers=HEADERS, files=files)
        
        is_success = response.status_code == 400
        print_result("Invalid File Type", is_success, f"Status: {response.status_code}")
        if response.status_code == 400:
            print(f"   Error Message: {response.json()['detail']}")
        
        test_file.unlink()
        return is_success
    except Exception as e:
        print_result("Invalid File Type", False, str(e))
        return False

def test_analyze_nonexistent_image():
    """Test 5: Analyze non-existent image"""
    print_section("TEST 5: Analyze Non-Existent Image (Expected: 404)")
    try:
        payload = {"image_id": "nonexistent-id-12345"}
        response = requests.post(f"{API_URL}/api/analyze", headers=HEADERS, json=payload)
        
        is_success = response.status_code == 404
        print_result("Non-Existent Image", is_success, f"Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   Error Message: {response.json()['detail']}")
        return is_success
    except Exception as e:
        print_result("Non-Existent Image", False, str(e))
        return False

def test_analyze_without_api_key():
    """Test 6: Analyze without API key"""
    print_section("TEST 6: Analyze Without API Key (Expected: 422 or 401)")
    try:
        payload = {"image_id": "some-id"}
        response = requests.post(f"{API_URL}/api/analyze", json=payload)  # No API key
        
        is_success = response.status_code in [401, 422]
        print_result("API Key Required", is_success, f"Status: {response.status_code}")
        if response.status_code in [401, 422]:
            print(f"   Error: {response.json().get('detail', 'API key required')}")
        return is_success
    except Exception as e:
        print_result("API Key Required", False, str(e))
        return False

def test_swagger_docs():
    """Test 7: Swagger UI documentation"""
    print_section("TEST 7: Swagger UI - GET /docs")
    try:
        response = requests.get(f"{API_URL}/docs", headers=HEADERS)
        is_success = response.status_code == 200
        print_result("Swagger UI", is_success, f"Status: {response.status_code}")
        if is_success:
            print("   ✓ Interactive API docs available at http://localhost:8000/docs")
        return is_success
    except Exception as e:
        print_result("Swagger UI", False, str(e))
        return False

def test_openapi_schema():
    """Test 8: OpenAPI schema"""
    print_section("TEST 8: OpenAPI Schema - GET /openapi.json")
    try:
        response = requests.get(f"{API_URL}/openapi.json", headers=HEADERS)
        is_success = response.status_code == 200
        print_result("OpenAPI Schema", is_success, f"Status: {response.status_code}")
        if is_success:
            data = response.json()
            print(f"   API Title: {data.get('info', {}).get('title')}")
            print(f"   API Version: {data.get('info', {}).get('version')}")
            print(f"   Available Paths: {list(data.get('paths', {}).keys())}")
        return is_success
    except Exception as e:
        print_result("OpenAPI Schema", False, str(e))
        return False

def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  Image Analysis API - Comprehensive Test Suite".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    # Run all tests
    results.append(("Health Check", test_health_check()))
    results.append(("Health Status", test_health_endpoint()))
    results.append(("Upload Auth", test_upload_without_api_key()))
    results.append(("Invalid File Type", test_upload_invalid_file_type()))
    results.append(("Non-Existent Image", test_analyze_nonexistent_image()))
    results.append(("Analyze Auth", test_analyze_without_api_key()))
    results.append(("Swagger Docs", test_swagger_docs()))
    results.append(("OpenAPI Schema", test_openapi_schema()))
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        symbol = "✅" if result else "❌"
        print(f"{symbol} {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    # Next steps
    print_section("NEXT STEPS - MANUAL TESTING")
    print("""
To test image upload and analysis:

1. Open: http://localhost:8000/docs
2. Try /api/upload:
   - Click 'Try it out'
   - Select a JPEG or PNG image file
   - Include X-API-Key header: test-api-key-12345
   - Click 'Execute'
   - Copy the returned 'image_id'

3. Try /api/analyze:
   - Click 'Try it out'
   - Enter the image_id from step 2
   - Click 'Execute'
   - View the mock analysis results

Test Cases to Verify:
✓ Upload valid JPEG/PNG image
✓ Upload file over 5MB (should fail)
✓ Analyze with valid image_id
✓ Get consistent analysis results
✓ Test error handling
    """)
    
    print("="*60)
    print("Test suite complete!\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to http://localhost:8000")
        print("   Make sure the server is running: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
