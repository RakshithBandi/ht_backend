"""
ChitFund HTTP Methods Test
Tests all HTTP methods (GET, POST, PUT, DELETE) specifically for ChitFund endpoint
with correct field names matching the model.
"""

import requests
from datetime import datetime

BASE_URL = "http://localhost:8000/api"
ADMIN_EMAIL = "htuser@gmail.com"
ADMIN_PASSWORD = "htportal@123"  # UPDATE THIS with your actual password

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

def print_info(text):
    print(f"{Colors.CYAN}ℹ {text}{Colors.RESET}")

def main():
    print_header("ChitFund HTTP Methods Test")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Setup authentication
    print_header("Authenticating")
    session = requests.Session()
    
    try:
        response = session.post(
            f"{BASE_URL}/login/",
            json={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print_success(f"Authenticated as {ADMIN_EMAIL}")
            user_data = response.json()
            print_info(f"User groups: {user_data.get('groups', [])}")
        else:
            print_error(f"Login failed - Status: {response.status_code}")
            print_error(f"Response: {response.text}")
            return
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return
    
    # Test data with correct field names
    test_data = {
        "year": 2024,
        "permanentAmount": 50000.00,
        "temporaryAmount": 30000.00,
        "juniorAmount": 10000.00,
        "villageContribution": 25000.00,
        "otherContributions": 15000.00,
        "inputGrandTotal": 10000.00,
        "grandTotal": 140000.00,
        "amountSpent": 20000.00
    }
    
    update_data = {
        "year": 2024,
        "permanentAmount": 60000.00,
        "temporaryAmount": 35000.00,
        "juniorAmount": 12000.00,
        "villageContribution": 30000.00,
        "otherContributions": 18000.00,
        "inputGrandTotal": 12000.00,
        "grandTotal": 167000.00,
        "amountSpent": 25000.00
    }
    
    results = {
        'GET_LIST': False,
        'POST': False,
        'GET_DETAIL': False,
        'PUT': False,
        'DELETE': False
    }
    
    created_id = None
    
    # Test GET (List)
    print_header("Testing GET (List)")
    try:
        response = session.get(f"{BASE_URL}/chitfund/")
        if response.status_code == 200:
            print_success(f"GET /chitfund/ - Status: {response.status_code}")
            data = response.json()
            print_info(f"Found {len(data)} existing ChitFund entries")
            results['GET_LIST'] = True
        else:
            print_error(f"GET /chitfund/ - Status: {response.status_code}")
            print(f"Response: {response.text[:300]}")
    except Exception as e:
        print_error(f"GET /chitfund/ - Error: {str(e)}")
    
    # Test POST (Create)
    print_header("Testing POST (Create)")
    try:
        response = session.post(
            f"{BASE_URL}/chitfund/",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code in [200, 201]:
            print_success(f"POST /chitfund/ - Status: {response.status_code}")
            results['POST'] = True
            response_data = response.json()
            created_id = response_data.get('id')
            print_info(f"Created ChitFund ID: {created_id}")
            print_info(f"Year: {response_data.get('year')}")
            print_info(f"Grand Total: {response_data.get('grandTotal')}")
        else:
            print_error(f"POST /chitfund/ - Status: {response.status_code}")
            print(f"Response: {response.text[:500]}")
    except Exception as e:
        print_error(f"POST /chitfund/ - Error: {str(e)}")
    
    if created_id:
        # Test GET (Detail)
        print_header("Testing GET (Detail)")
        try:
            response = session.get(f"{BASE_URL}/chitfund/{created_id}/")
            if response.status_code == 200:
                print_success(f"GET /chitfund/{created_id}/ - Status: {response.status_code}")
                results['GET_DETAIL'] = True
                data = response.json()
                print_info(f"Retrieved ChitFund for year: {data.get('year')}")
            else:
                print_error(f"GET /chitfund/{created_id}/ - Status: {response.status_code}")
        except Exception as e:
            print_error(f"GET /chitfund/{created_id}/ - Error: {str(e)}")
        
        # Test PUT (Update)
        print_header("Testing PUT (Update)")
        try:
            response = session.put(
                f"{BASE_URL}/chitfund/{created_id}/",
                json=update_data,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                print_success(f"PUT /chitfund/{created_id}/ - Status: {response.status_code}")
                results['PUT'] = True
                response_data = response.json()
                print_info(f"Updated Grand Total: {response_data.get('grandTotal')}")
            else:
                print_error(f"PUT /chitfund/{created_id}/ - Status: {response.status_code}")
                print(f"Response: {response.text[:500]}")
        except Exception as e:
            print_error(f"PUT /chitfund/{created_id}/ - Error: {str(e)}")
        
        # Test DELETE
        print_header("Testing DELETE")
        try:
            response = session.delete(f"{BASE_URL}/chitfund/{created_id}/")
            if response.status_code in [200, 204]:
                print_success(f"DELETE /chitfund/{created_id}/ - Status: {response.status_code}")
                results['DELETE'] = True
            else:
                print_error(f"DELETE /chitfund/{created_id}/ - Status: {response.status_code}")
        except Exception as e:
            print_error(f"DELETE /chitfund/{created_id}/ - Error: {str(e)}")
    else:
        print_error("Skipping GET detail, PUT, and DELETE tests (no ID created)")
    
    # Print Summary
    print_header("Test Summary")
    
    for method, success in results.items():
        if success:
            print_success(f"{method}")
        else:
            print_error(f"{method}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n{Colors.CYAN}Passed: {passed}/{total}{Colors.RESET}")
    
    if passed == total:
        print(f"{Colors.GREEN}🎉 All ChitFund HTTP methods working!{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}⚠ Some tests failed. Check the output above for details.{Colors.RESET}")
    
    print(f"\n{Colors.BLUE}Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}\n")

if __name__ == "__main__":
    main()
