"""
Test script for Expenditure API endpoints
Tests all HTTP methods: GET, POST, PUT, DELETE
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/expenditure/"
LOGIN_URL = f"{BASE_URL}/api/login/"

# Test credentials (update with your actual credentials)
USERNAME = "htuser@gmail.com"  # Change to your admin username
PASSWORD = "htportal@123"  # Change to your admin password

# Create a session to maintain cookies
session = requests.Session()

def print_separator(title=""):
    """Print a formatted separator"""
    print("\n" + "="*70)
    if title:
        print(f"  {title}")
        print("="*70)

def print_response(response, show_data=True):
    """Print response details"""
    print(f"Status Code: {response.status_code}")
    print(f"Status: {'✅ SUCCESS' if response.status_code < 400 else '❌ FAILED'}")
    if show_data:
        try:
            data = response.json()
            print(f"Response Data:\n{json.dumps(data, indent=2)}")
        except:
            print(f"Response Text: {response.text[:200]}")

def login():
    """Login to get session authentication"""
    print_separator("STEP 1: LOGIN")
    
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    try:
        response = session.post(LOGIN_URL, json=login_data)
        print_response(response)
        
        if response.status_code == 200:
            print("✅ Login successful! Session authenticated.")
            return True
        else:
            print("❌ Login failed! Please check credentials.")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def test_get_all():
    """Test GET request - Get all expenditures"""
    print_separator("STEP 2: GET ALL EXPENDITURES (GET)")
    
    try:
        response = session.get(API_URL)
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Total expenditures found: {len(data)}")
            return data
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def test_create():
    """Test POST request - Create new expenditure"""
    print_separator("STEP 3: CREATE EXPENDITURE (POST)")
    
    test_data = {
        "year": "2025",
        "purpose": "Test expenditure - API testing",
        "amountSpent": 5000.50
    }
    
    print(f"Creating expenditure with data:\n{json.dumps(test_data, indent=2)}")
    
    try:
        response = session.post(API_URL, json=test_data)
        print_response(response)
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"\n✅ Expenditure created successfully!")
            print(f"ID: {data.get('id')}")
            return data.get('id')
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_single(expenditure_id):
    """Test GET request - Get single expenditure by ID"""
    print_separator(f"STEP 4: GET SINGLE EXPENDITURE (GET) - ID: {expenditure_id}")
    
    try:
        response = session.get(f"{API_URL}{expenditure_id}/")
        print_response(response)
        
        if response.status_code == 200:
            print("✅ Successfully retrieved expenditure details")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_update(expenditure_id):
    """Test PUT request - Update expenditure"""
    print_separator(f"STEP 5: UPDATE EXPENDITURE (PUT) - ID: {expenditure_id}")
    
    update_data = {
        "year": "2025",
        "purpose": "Updated test expenditure - Modified via API",
        "amountSpent": 7500.75
    }
    
    print(f"Updating expenditure with data:\n{json.dumps(update_data, indent=2)}")
    
    try:
        response = session.put(f"{API_URL}{expenditure_id}/", json=update_data)
        print_response(response)
        
        if response.status_code == 200:
            print("✅ Expenditure updated successfully!")
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_delete(expenditure_id):
    """Test DELETE request - Delete expenditure"""
    print_separator(f"STEP 6: DELETE EXPENDITURE (DELETE) - ID: {expenditure_id}")
    
    try:
        response = session.delete(f"{API_URL}{expenditure_id}/")
        print(f"Status Code: {response.status_code}")
        print(f"Status: {'✅ SUCCESS' if response.status_code in [200, 204] else '❌ FAILED'}")
        
        if response.status_code in [200, 204]:
            print("✅ Expenditure deleted successfully!")
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verify_deletion(expenditure_id):
    """Verify that the expenditure was actually deleted"""
    print_separator(f"STEP 7: VERIFY DELETION - ID: {expenditure_id}")
    
    try:
        response = session.get(f"{API_URL}{expenditure_id}/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ Verified: Expenditure no longer exists (404 Not Found)")
            return True
        else:
            print("❌ Warning: Expenditure still exists!")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Run all API tests in sequence"""
    print("\n" + "🚀 " + "="*66)
    print("  EXPENDITURE API - HTTP METHODS TEST")
    print("="*70)
    print(f"Testing API: {API_URL}")
    print(f"Username: {USERNAME}")
    
    results = {
        "login": False,
        "get_all": False,
        "create": False,
        "get_single": False,
        "update": False,
        "delete": False,
        "verify_deletion": False
    }
    
    # Step 1: Login
    if not login():
        print("\n❌ Cannot proceed without authentication!")
        return results
    results["login"] = True
    
    # Step 2: Get all expenditures
    initial_expenditures = test_get_all()
    results["get_all"] = True
    
    # Step 3: Create new expenditure
    expenditure_id = test_create()
    if expenditure_id:
        results["create"] = True
        
        # Step 4: Get single expenditure
        if test_get_single(expenditure_id):
            results["get_single"] = True
        
        # Step 5: Update expenditure
        if test_update(expenditure_id):
            results["update"] = True
        
        # Step 6: Delete expenditure
        if test_delete(expenditure_id):
            results["delete"] = True
            
            # Step 7: Verify deletion
            if verify_deletion(expenditure_id):
                results["verify_deletion"] = True
    
    # Print summary
    print_separator("TEST SUMMARY")
    print("\nResults:")
    print(f"  1. Login (POST):           {'✅ PASS' if results['login'] else '❌ FAIL'}")
    print(f"  2. Get All (GET):          {'✅ PASS' if results['get_all'] else '❌ FAIL'}")
    print(f"  3. Create (POST):          {'✅ PASS' if results['create'] else '❌ FAIL'}")
    print(f"  4. Get Single (GET):       {'✅ PASS' if results['get_single'] else '❌ FAIL'}")
    print(f"  5. Update (PUT):           {'✅ PASS' if results['update'] else '❌ FAIL'}")
    print(f"  6. Delete (DELETE):        {'✅ PASS' if results['delete'] else '❌ FAIL'}")
    print(f"  7. Verify Deletion (GET):  {'✅ PASS' if results['verify_deletion'] else '❌ FAIL'}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\n{'='*70}")
    print(f"  OVERALL: {passed_tests}/{total_tests} tests passed")
    print(f"{'='*70}\n")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! The Expenditure API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return results

if __name__ == "__main__":
    print("\n⚙️  Make sure the Django server is running on http://localhost:8000")
    print("⚙️  Update USERNAME and PASSWORD in this script if needed\n")
    
    input("Press Enter to start testing...")
    
    run_all_tests()
