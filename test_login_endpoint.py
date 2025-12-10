"""
Direct API Login Test
Tests the actual login endpoint to see what's happening
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

print("\n=== Testing Login Endpoint ===\n")

# Test data
credentials = {
    "username": "htuser@gmail.com",
    "password": "htportal@123"
}

print(f"Sending to: {BASE_URL}/login/")
print(f"Credentials: {json.dumps(credentials, indent=2)}")

try:
    response = requests.post(
        f"{BASE_URL}/login/",
        json=credentials,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        print("\n✓ Login successful!")
        print(f"Cookies: {response.cookies.get_dict()}")
    else:
        print("\n✗ Login failed!")
        
        # Try with username instead of email
        print("\n--- Trying with username instead of email ---")
        credentials2 = {
            "username": "htuser",
            "password": "htportal@123"
        }
        
        response2 = requests.post(
            f"{BASE_URL}/login/",
            json=credentials2,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Response Status: {response2.status_code}")
        print(f"Response Body: {response2.text}")
        
except Exception as e:
    print(f"Error: {str(e)}")
