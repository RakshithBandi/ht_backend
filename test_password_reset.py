"""
Test script for Password Reset functionality
Tests the complete forgot password flow
"""

import requests
import json
import re

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

# Test email (must exist in database)
TEST_EMAIL = "htuser@gmail.com"  # Change to an email that exists in your database
TEST_NEW_PASSWORD = "newpassword123"

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

def test_request_reset():
    """Test requesting password reset"""
    print_separator("STEP 1: REQUEST PASSWORD RESET")
    
    print(f"Requesting password reset for: {TEST_EMAIL}")
    
    try:
        response = requests.post(
            f"{API_URL}/password-reset/request/",
            json={"email": TEST_EMAIL}
        )
        print_response(response)
        
        if response.status_code == 200:
            print("\n✅ Password reset request successful!")
            print("\n📧 CHECK YOUR BACKEND CONSOLE for the reset link")
            print("   (Email will be printed to console since we're using console backend)")
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_invalid_email():
    """Test requesting reset with invalid email"""
    print_separator("STEP 2: TEST INVALID EMAIL (Security Check)")
    
    invalid_email = "nonexistent@example.com"
    print(f"Requesting password reset for non-existent email: {invalid_email}")
    
    try:
        response = requests.post(
            f"{API_URL}/password-reset/request/",
            json={"email": invalid_email}
        )
        print_response(response)
        
        # Should still return 200 for security (don't reveal if email exists)
        if response.status_code == 200:
            print("\n✅ Correctly returns success even for non-existent email (security)")
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_verify_token(uid, token):
    """Test verifying reset token"""
    print_separator("STEP 3: VERIFY RESET TOKEN")
    
    print(f"Verifying token...")
    print(f"UID: {uid}")
    print(f"Token: {token[:20]}...")
    
    try:
        response = requests.post(
            f"{API_URL}/password-reset/verify/",
            json={"uid": uid, "token": token}
        )
        print_response(response)
        
        if response.status_code == 200:
            print("\n✅ Token is valid!")
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_reset_password(uid, token):
    """Test resetting password"""
    print_separator("STEP 4: RESET PASSWORD")
    
    print(f"Resetting password to: {TEST_NEW_PASSWORD}")
    
    try:
        response = requests.post(
            f"{API_URL}/password-reset/reset/",
            json={
                "uid": uid,
                "token": token,
                "password": TEST_NEW_PASSWORD
            }
        )
        print_response(response)
        
        if response.status_code == 200:
            print("\n✅ Password reset successful!")
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_login_with_new_password():
    """Test logging in with new password"""
    print_separator("STEP 5: TEST LOGIN WITH NEW PASSWORD")
    
    print(f"Attempting login with new password...")
    
    try:
        response = requests.post(
            f"{API_URL}/login/",
            json={
                "username": TEST_EMAIL,
                "password": TEST_NEW_PASSWORD
            }
        )
        print_response(response)
        
        if response.status_code == 200:
            print("\n✅ Login successful with new password!")
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_manual_test():
    """Run manual test with user input"""
    print("\n" + "🚀 " + "="*66)
    print("  PASSWORD RESET - MANUAL TEST")
    print("="*70)
    print(f"Testing API: {API_URL}")
    print(f"Test Email: {TEST_EMAIL}")
    
    results = {
        "request_reset": False,
        "invalid_email": False,
        "verify_token": False,
        "reset_password": False,
        "login_new_password": False,
    }
    
    # Step 1: Request password reset
    if test_request_reset():
        results["request_reset"] = True
    else:
        print("\n❌ Cannot proceed without successful reset request!")
        return results
    
    # Step 2: Test invalid email
    if test_invalid_email():
        results["invalid_email"] = True
    
    # Step 3-5: Manual token entry
    print_separator("MANUAL TOKEN ENTRY REQUIRED")
    print("\n📋 Instructions:")
    print("1. Check your backend console for the password reset email")
    print("2. Find the reset link that looks like:")
    print("   http://localhost:5173/reset-password/{uid}/{token}")
    print("3. Copy the UID and TOKEN from the link\n")
    
    uid = input("Enter UID from reset link: ").strip()
    token = input("Enter TOKEN from reset link: ").strip()
    
    if not uid or not token:
        print("\n❌ UID and TOKEN are required!")
        return results
    
    # Step 3: Verify token
    if test_verify_token(uid, token):
        results["verify_token"] = True
        
        # Step 4: Reset password
        if test_reset_password(uid, token):
            results["reset_password"] = True
            
            # Step 5: Test login
            if test_login_with_new_password():
                results["login_new_password"] = True
    
    # Print summary
    print_separator("TEST SUMMARY")
    print("\nResults:")
    print(f"  1. Request Reset:          {'✅ PASS' if results['request_reset'] else '❌ FAIL'}")
    print(f"  2. Invalid Email Test:     {'✅ PASS' if results['invalid_email'] else '❌ FAIL'}")
    print(f"  3. Verify Token:           {'✅ PASS' if results['verify_token'] else '❌ FAIL'}")
    print(f"  4. Reset Password:         {'✅ PASS' if results['reset_password'] else '❌ FAIL'}")
    print(f"  5. Login New Password:     {'✅ PASS' if results['login_new_password'] else '❌ FAIL'}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\n{'='*70}")
    print(f"  OVERALL: {passed_tests}/{total_tests} tests passed")
    print(f"{'='*70}\n")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Password reset is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return results

if __name__ == "__main__":
    print("\n⚙️  SETUP INSTRUCTIONS:")
    print("1. Make sure Django server is running: python manage.py runserver")
    print("2. Update TEST_EMAIL in this script to an email that exists in your database")
    print("3. Keep the backend console visible to see the reset email\n")
    
    input("Press Enter to start testing...")
    
    run_manual_test()
