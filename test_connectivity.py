"""
Simple connectivity test for the Django backend
"""
import requests

BASE_URL = "http://localhost:8000/api"

print("Testing Django Backend Connectivity...")
print(f"Base URL: {BASE_URL}\n")

try:
    # Test if server is running
    response = requests.get(f"{BASE_URL}/sponsors/", timeout=5)
    print(f"✓ Server is running!")
    print(f"  Status Code: {response.status_code}")
    print(f"  Response: {response.text[:200]}")
except requests.exceptions.ConnectionError:
    print("✗ Server is NOT running!")
    print("\nPlease start the Django server first:")
    print("  cd c:\\Users\\rakshith bandi\\OneDrive\\Desktop\\HT_frontend\\backend")
    print("  python manage.py runserver")
except Exception as e:
    print(f"✗ Error: {e}")
