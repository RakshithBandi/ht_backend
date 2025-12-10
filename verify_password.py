import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ht_backend.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

print("\n=== Comprehensive Authentication Test ===\n")

# Get the htuser
try:
    user_obj = User.objects.get(email="htuser@gmail.com")
    print(f"✓ Found user:")
    print(f"  Username: {user_obj.username}")
    print(f"  Email: {user_obj.email}")
    print(f"  Is Active: {user_obj.is_active}")
    print(f"  Is Superuser: {user_obj.is_superuser}")
    print(f"  Groups: {list(user_obj.groups.values_list('name', flat=True))}")
    
    # Test multiple possible passwords
    passwords_to_test = [
        "htportal@123",
        "admin123",
        "htuser",
        "password",
    ]
    
    print(f"\nTesting passwords for username '{user_obj.username}':")
    print("-" * 60)
    
    for pwd in passwords_to_test:
        user = authenticate(username=user_obj.username, password=pwd)
        if user:
            print(f"✓ CORRECT PASSWORD: '{pwd}'")
            print(f"\nUpdate your test files with:")
            print(f'  ADMIN_EMAIL = "{user_obj.email}"')
            print(f'  ADMIN_PASSWORD = "{pwd}"')
            break
        else:
            print(f"✗ Wrong: '{pwd}'")
    else:
        print(f"\n⚠ None of the common passwords worked!")
        print(f"\nYou need to reset the password:")
        print(f"  python manage.py changepassword {user_obj.username}")
        print(f"\nOr create a new superuser:")
        print(f"  python manage.py createsuperuser")
        
except User.DoesNotExist:
    print("✗ User with email 'htuser@gmail.com' not found!")
    print("\nCreate a superuser:")
    print("  python manage.py createsuperuser")
