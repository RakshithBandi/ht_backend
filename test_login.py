"""
Quick test to verify login credentials and authentication
"""
import requests

BASE_URL = "http://localhost:8000/api"

# Try different possible admin credentials
credentials_to_test = [
    {"username": "admin@ht.com", "password": "admin123"},
    {"username": "admin", "password": "admin123"},
    {"username": "admin@example.com", "password": "admin123"},
]

print("Testing Login Credentials...\n")

for creds in credentials_to_test:
    print(f"Trying: {creds['username']}")
    try:
        response = requests.post(
            f"{BASE_URL}/login/",
            json=creds,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"  ✓ SUCCESS! Status: {response.status_code}")
            print(f"  Response: {response.json()}")
            print(f"\n  Use these credentials:")
            print(f"    Email: {creds['username']}")
            print(f"    Password: {creds['password']}\n")
            break
        else:
            print(f"  ✗ Failed - Status: {response.status_code}")
            print(f"  Response: {response.text[:200]}\n")
    except Exception as e:
        print(f"  ✗ Error: {str(e)}\n")
