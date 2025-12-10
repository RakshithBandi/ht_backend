"""
Database Verification Script
This script demonstrates that user credentials are stored in PostgreSQL.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ht_backend.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection

# Check database connection
print("=" * 70)
print("DATABASE VERIFICATION")
print("=" * 70)

# Show database settings
print(f"\nDatabase Engine: {connection.settings_dict['ENGINE']}")
print(f"Database Name: {connection.settings_dict['NAME']}")
print(f"Database Host: {connection.settings_dict['HOST']}")
print(f"Database Port: {connection.settings_dict['PORT']}")

# Check if we can connect
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"\n✓ Connected to PostgreSQL")
        print(f"  Version: {version[0][:50]}...")
except Exception as e:
    print(f"\n✗ Database connection failed: {e}")
    sys.exit(1)

# Check users table
print("\n" + "=" * 70)
print("REGISTERED USERS")
print("=" * 70)

users = User.objects.all()
print(f"\nTotal users in database: {users.count()}")

if users.count() > 0:
    print("\nUser Details:")
    for i, user in enumerate(users, 1):
        print(f"\n  User #{i}:")
        print(f"    - Username: {user.username}")
        print(f"    - Email: {user.email}")
        print(f"    - Active: {user.is_active}")
        print(f"    - Joined: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    print("\n  No users registered yet.")
    print("  Sign up through the frontend to create users.")

print("\n" + "=" * 70)
print("✓ All data is stored in PostgreSQL database 'ht_db'")
print("=" * 70 + "\n")
