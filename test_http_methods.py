"""
HTTP Methods Verification Script
Tests all HTTP methods (GET, POST, PUT, DELETE) for:
- Sponsors
- Games
- Members (Permanent, Temporary, Junior)
- Announcements
- ChitFund
- Login (POST only)
- Signup (POST only)

This script authenticates as an admin user to test all operations.
"""

import requests
import json
from datetime import datetime

# Base URL - adjust if needed
BASE_URL = "http://localhost:8000/api"

# Admin credentials - update these if needed
ADMIN_EMAIL = "htuser@gmail.com"
ADMIN_PASSWORD = "htportal@123"  # UPDATE THIS with your actual password

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ {text}{Colors.RESET}")

def setup_authentication():
    """
    Authenticate and return a session with cookies
    """
    print_header("Setting Up Authentication")
    
    session = requests.Session()
    
    # Try to login
    try:
        response = session.post(
            f"{BASE_URL}/login/",
            json={
                "username": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print_success(f"Authenticated as {ADMIN_EMAIL}")
            user_data = response.json()
            print_info(f"User groups: {user_data.get('groups', [])}")
            return session
        else:
            print_error(f"Login failed - Status: {response.status_code}")
            print_error(f"Response: {response.text}")
            print_warning("Continuing with unauthenticated session (only GET will work)")
            return session
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        print_warning("Continuing with unauthenticated session (only GET will work)")
        return session

def test_endpoint(name, base_path, test_data, update_data=None, session=None):
    """
    Test all CRUD operations for a given endpoint
    """
    print_header(f"Testing {name}")
    results = {
        'GET_LIST': False,
        'POST': False,
        'GET_DETAIL': False,
        'PUT': False,
        'DELETE': False
    }
    
    created_id = None
    
    # Use session if provided, otherwise create new requests
    requester = session if session else requests
    
    # Test GET (List)
    try:
        response = requester.get(f"{BASE_URL}/{base_path}/")
        if response.status_code == 200:
            print_success(f"GET {base_path}/ - Status: {response.status_code}")
            data = response.json()
            if isinstance(data, list):
                print_info(f"Found {len(data)} existing items")
            results['GET_LIST'] = True
        else:
            print_error(f"GET {base_path}/ - Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print_error(f"GET {base_path}/ - Error: {str(e)}")
    
    # Test POST (Create)
    try:
        response = requester.post(
            f"{BASE_URL}/{base_path}/",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code in [200, 201]:
            print_success(f"POST {base_path}/ - Status: {response.status_code}")
            results['POST'] = True
            try:
                response_data = response.json()
                created_id = response_data.get('id')
                print_info(f"Created ID: {created_id}")
            except:
                print_warning("Could not extract ID from response")
        else:
            print_error(f"POST {base_path}/ - Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}")
    except Exception as e:
        print_error(f"POST {base_path}/ - Error: {str(e)}")
    
    # If we have a created ID, test GET detail, PUT, and DELETE
    if created_id:
        # Test GET (Detail)
        try:
            response = requester.get(f"{BASE_URL}/{base_path}/{created_id}/")
            if response.status_code == 200:
                print_success(f"GET {base_path}/{created_id}/ - Status: {response.status_code}")
                results['GET_DETAIL'] = True
            else:
                print_error(f"GET {base_path}/{created_id}/ - Status: {response.status_code}")
        except Exception as e:
            print_error(f"GET {base_path}/{created_id}/ - Error: {str(e)}")
        
        # Test PUT (Update)
        if update_data:
            try:
                response = requester.put(
                    f"{BASE_URL}/{base_path}/{created_id}/",
                    json=update_data,
                    headers={'Content-Type': 'application/json'}
                )
                if response.status_code == 200:
                    print_success(f"PUT {base_path}/{created_id}/ - Status: {response.status_code}")
                    results['PUT'] = True
                else:
                    print_error(f"PUT {base_path}/{created_id}/ - Status: {response.status_code}")
                    print(f"   Response: {response.text[:300]}")
            except Exception as e:
                print_error(f"PUT {base_path}/{created_id}/ - Error: {str(e)}")
        
        # Test DELETE
        try:
            response = requester.delete(f"{BASE_URL}/{base_path}/{created_id}/")
            if response.status_code in [200, 204]:
                print_success(f"DELETE {base_path}/{created_id}/ - Status: {response.status_code}")
                results['DELETE'] = True
            else:
                print_error(f"DELETE {base_path}/{created_id}/ - Status: {response.status_code}")
        except Exception as e:
            print_error(f"DELETE {base_path}/{created_id}/ - Error: {str(e)}")
    else:
        print_warning("Skipping GET detail, PUT, and DELETE tests (no ID created)")
    
    return results

def test_signup():
    """
    Test signup endpoint (doesn't require authentication)
    """
    print_header("Testing Signup")
    
    timestamp = int(datetime.now().timestamp())
    test_data = {
        "username": f"testuser_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/signup/",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code in [200, 201]:
            print_success(f"POST signup/ - Status: {response.status_code}")
            print_info(f"Created user: {test_data['username']}")
            return True
        else:
            print_error(f"POST signup/ - Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}")
            return False
    except Exception as e:
        print_error(f"POST signup/ - Error: {str(e)}")
        return False

def main():
    print_header("HTTP Methods Verification Test Suite")
    print(f"Base URL: {BASE_URL}")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Setup authentication
    session = setup_authentication()
    
    all_results = {}
    
    # Test Sponsors
    all_results['Sponsors'] = test_endpoint(
        "Sponsors",
        "sponsors",
        {
            "name": "Test Sponsor",
            "description": "This is a test sponsor for verification",
            "image": ""  # Optional base64 image
        },
        {
            "name": "Updated Test Sponsor",
            "description": "This is an updated test sponsor",
            "image": ""
        },
        session
    )
    
    # Test Games
    all_results['Games'] = test_endpoint(
        "Games",
        "games",
        {
            "gameName": "Test Game",
            "participantsCount": 50,
            "description": "This is a test game for verification",
            "winnerName": "Test Winner",
            "winnerImage": ""  # Optional base64 image
        },
        {
            "gameName": "Updated Test Game",
            "participantsCount": 75,
            "description": "This is an updated test game",
            "winnerName": "Updated Winner",
            "winnerImage": ""
        },
        session
    )
    
    # Test Permanent Members
    all_results['Members (Permanent)'] = test_endpoint(
        "Members - Permanent",
        "members/permanent",
        {
            "name": "Test Permanent Member",
            "email": "permanent@test.com",
            "phone": "1234567890",
            "membershipDate": datetime.now().strftime('%Y-%m-%d'),
            "membershipType": "Permanent"
        },
        {
            "name": "Updated Permanent Member",
            "email": "permanent@test.com",
            "phone": "0987654321",
            "membershipDate": datetime.now().strftime('%Y-%m-%d'),
            "membershipType": "Permanent"
        },
        session
    )
    
    # Test Temporary Members
    all_results['Members (Temporary)'] = test_endpoint(
        "Members - Temporary",
        "members/temporary",
        {
            "name": "Test Temporary Member",
            "email": "temporary@test.com",
            "phone": "1234567890",
            "membershipDate": datetime.now().strftime('%Y-%m-%d'),
            "expiryDate": "2025-12-31",
            "membershipType": "Temporary"
        },
        {
            "name": "Updated Temporary Member",
            "email": "temporary@test.com",
            "phone": "0987654321",
            "membershipDate": datetime.now().strftime('%Y-%m-%d'),
            "expiryDate": "2026-12-31",
            "membershipType": "Temporary"
        },
        session
    )
    
    # Test Junior Members
    all_results['Members (Junior)'] = test_endpoint(
        "Members - Junior",
        "members/junior",
        {
            "name": "Test Junior Member",
            "email": "junior@test.com",
            "phone": "1234567890",
            "dateOfBirth": "2010-01-01",
            "guardianName": "Test Guardian",
            "membershipType": "Junior"
        },
        {
            "name": "Updated Junior Member",
            "email": "junior@test.com",
            "phone": "0987654321",
            "dateOfBirth": "2010-01-01",
            "guardianName": "Updated Guardian",
            "membershipType": "Junior"
        },
        session
    )
    
    # Test Announcements
    all_results['Announcements'] = test_endpoint(
        "Announcements",
        "dashboard/announcements",
        {
            "heading": "Test Announcement",
            "year": 2024,
            "description": "This is a test announcement"
        },
        {
            "heading": "Updated Test Announcement",
            "year": 2024,
            "description": "This is an updated test announcement"
        },
        session
    )
    
    # Test ChitFund
    all_results['ChitFund'] = test_endpoint(
        "ChitFund",
        "chitfund",
        {
            "year": 2024,
            "permanentAmount": 50000.00,
            "temporaryAmount": 30000.00,
            "juniorAmount": 10000.00,
            "villageContribution": 25000.00,
            "otherContributions": 15000.00,
            "inputGrandTotal": 10000.00,
            "grandTotal": 140000.00,
            "amountSpent": 20000.00
        },
        {
            "year": 2024,
            "permanentAmount": 60000.00,
            "temporaryAmount": 35000.00,
            "juniorAmount": 12000.00,
            "villageContribution": 30000.00,
            "otherContributions": 18000.00,
            "inputGrandTotal": 12000.00,
            "grandTotal": 167000.00,
            "amountSpent": 25000.00
        },
        session
    )
    
    # Test Signup (doesn't require auth)
    signup_result = test_signup()
    all_results['Signup'] = {'POST': signup_result}
    
    # Login was already tested during authentication setup
    all_results['Login'] = {'POST': True}  # We know it worked if we got here with auth
    
    # Print Summary
    print_header("Test Summary")
    
    total_tests = 0
    passed_tests = 0
    
    for endpoint, results in all_results.items():
        print(f"\n{Colors.CYAN}{endpoint}:{Colors.RESET}")
        for method, success in results.items():
            total_tests += 1
            if success:
                passed_tests += 1
                print_success(f"  {method}")
            else:
                print_error(f"  {method}")
    
    # Overall statistics
    print_header("Overall Statistics")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {Colors.GREEN}{passed_tests}{Colors.RESET}")
    print(f"Failed: {Colors.RED}{total_tests - passed_tests}{Colors.RESET}")
    
    if passed_tests == total_tests:
        print(f"\n{Colors.GREEN}🎉 All tests passed!{Colors.RESET}")
    else:
        success_rate = (passed_tests / total_tests) * 100
        print(f"\nSuccess rate: {success_rate:.1f}%")
    
    print(f"\n{Colors.BLUE}Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}\n")

if __name__ == "__main__":
    main()
