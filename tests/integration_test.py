#!/usr/bin/env python3
"""
Integration Tests for Raspberry Pi Art Display
Tests all backend endpoints and functionality
"""
import requests
import time
import sys

BASE_URL = "http://localhost:5000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}Testing: {name}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ {message}{Colors.END}")

def test_health_check():
    """Test health check endpoint"""
    print_test("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                print_success("Server is healthy")
                return True
    except Exception as e:
        print_error(f"Health check failed: {e}")
    return False

def test_configuration():
    """Test configuration endpoint"""
    print_test("Configuration Management")
    try:
        response = requests.get(f"{BASE_URL}/api/config", timeout=5)
        if response.status_code == 200:
            config = response.json()
            required_keys = ['image_duration', 'device_ip', 'paths', 'time_periods', 'presence']

            for key in required_keys:
                if key in config:
                    print_success(f"Config has '{key}'")
                else:
                    print_error(f"Config missing '{key}'")
                    return False

            print_info(f"Image duration: {config['image_duration']}s")
            print_info(f"Device IP: {config['device_ip']}")
            return True
    except Exception as e:
        print_error(f"Configuration test failed: {e}")
    return False

def test_images():
    """Test image endpoints"""
    print_test("Image File Handling")
    try:
        response = requests.get(f"{BASE_URL}/api/images", timeout=5)
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            images = data.get('images', [])

            print_success(f"Found {count} images")

            if count > 0:
                # Test fetching first image
                first_image = images[0]
                print_info(f"Testing image: {first_image['filename']}")

                img_response = requests.get(f"{BASE_URL}{first_image['url']}", timeout=5)
                if img_response.status_code == 200:
                    print_success(f"Successfully fetched image ({len(img_response.content)} bytes)")
                    return True
                else:
                    print_error(f"Failed to fetch image: {img_response.status_code}")
            else:
                print_error("No images found")
    except Exception as e:
        print_error(f"Image test failed: {e}")
    return False

def test_todos():
    """Test TODO endpoints"""
    print_test("TODO File Handling")
    try:
        response = requests.get(f"{BASE_URL}/api/todos", timeout=5)
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            items = data.get('items', [])

            print_success(f"Found {count} TODO items")
            for i, item in enumerate(items[:3], 1):
                print_info(f"  {i}. {item[:50]}{'...' if len(item) > 50 else ''}")
            return True
        elif response.status_code == 404:
            print_info("TODO file not found (optional)")
            return True
    except Exception as e:
        print_error(f"TODO test failed: {e}")
    return False

def test_time_period():
    """Test time period endpoint"""
    print_test("Time-of-Day Service")
    try:
        response = requests.get(f"{BASE_URL}/api/time-period", timeout=5)
        if response.status_code == 200:
            data = response.json()
            period = data.get('period')
            current_time = data.get('current_time')

            print_success(f"Current period: {period}")
            print_info(f"Time: {current_time}")

            if period in ['day', 'night']:
                return True
            else:
                print_error(f"Invalid period: {period}")
    except Exception as e:
        print_error(f"Time period test failed: {e}")
    return False

def test_presence():
    """Test presence detection endpoint"""
    print_test("Network Presence Detection")
    try:
        response = requests.get(f"{BASE_URL}/api/presence", timeout=5)
        if response.status_code == 200:
            data = response.json()
            present = data.get('present')
            device_ip = data.get('device_ip')
            last_check = data.get('last_check')

            print_success(f"Presence status: {'Present' if present else 'Away'}")
            print_info(f"Monitoring device: {device_ip}")
            print_info(f"Last checked: {last_check}")
            return True
    except Exception as e:
        print_error(f"Presence test failed: {e}")
    return False

def test_frontend():
    """Test frontend loads"""
    print_test("Frontend Assets")
    try:
        # Test HTML
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200 and 'Raspberry Pi Art Display' in response.text:
            print_success("HTML loads correctly")
        else:
            print_error("HTML failed to load")
            return False

        # Test CSS
        response = requests.get(f"{BASE_URL}/styles.css", timeout=5)
        if response.status_code == 200:
            print_success("CSS loads correctly")
        else:
            print_error("CSS failed to load")
            return False

        # Test JS
        response = requests.get(f"{BASE_URL}/app.js", timeout=5)
        if response.status_code == 200:
            print_success("JavaScript loads correctly")
        else:
            print_error("JavaScript failed to load")
            return False

        return True
    except Exception as e:
        print_error(f"Frontend test failed: {e}")
    return False

def test_continuous_operation():
    """Test system operates continuously"""
    print_test("Continuous Operation")
    try:
        print_info("Testing multiple API calls...")

        for i in range(5):
            response = requests.get(f"{BASE_URL}/api/presence", timeout=5)
            if response.status_code != 200:
                print_error(f"Failed on iteration {i+1}")
                return False
            time.sleep(1)

        print_success("System handles continuous requests")
        return True
    except Exception as e:
        print_error(f"Continuous operation test failed: {e}")
    return False

def run_all_tests():
    """Run all integration tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}Raspberry Pi Art Display - Integration Tests{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

    tests = [
        test_health_check,
        test_configuration,
        test_images,
        test_todos,
        test_time_period,
        test_presence,
        test_frontend,
        test_continuous_operation
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print_error(f"Test crashed: {e}")
            results.append(False)

    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"{Colors.GREEN}All tests passed! ({passed}/{total}){Colors.END}")
        return 0
    else:
        print(f"{Colors.YELLOW}Some tests failed: {passed}/{total} passed{Colors.END}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(run_all_tests())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.END}")
        sys.exit(1)
