# ChitFund Authentication Fix - Instructions

## Problem

The ChitFund test is failing with:
```
✗ POST chitfund/ - Status: 403
Response: {"detail":"Authentication credentials were not provided."}
```

This means the login is failing or credentials are incorrect.

## Steps to Fix

### Step 1: Check Existing Users

Run this command to see what users exist:
```bash
python check_users.py
```

This will show all users, their emails, and groups. Look for a user with Admin or Manager group.

### Step 2: Test Login Credentials

Run this command to test different login credentials:
```bash
python test_login.py
```

This will try common admin credentials and tell you which ones work.

### Step 3: Update Test Scripts

Once you find working credentials, update these files:

**File: `test_chitfund.py`** (lines 10-11)
```python
ADMIN_EMAIL = "your_working_email@example.com"  # Update this
ADMIN_PASSWORD = "your_working_password"  # Update this
```

**File: `test_http_methods.py`** (lines 20-21)
```python
ADMIN_EMAIL = "your_working_email@example.com"  # Update this
ADMIN_PASSWORD = "your_working_password"  # Update this
```

### Step 4: Create Admin User (if needed)

If no admin user exists, run:
```bash
python manage.py shell
```

Then paste this:
```python
from django.contrib.auth.models import User, Group

# Create Admin group
admin_group, _ = Group.objects.get_or_create(name='Admin')

# Create admin user
admin = User.objects.create_user(
    username='admin',
    email='admin@ht.com',
    password='admin123',
    is_staff=True,
    is_superuser=True
)
admin.groups.add(admin_group)
admin.save()

print("Admin user created!")
print("Email: admin@ht.com")
print("Password: admin123")
```

Press Ctrl+D (or Ctrl+Z on Windows) to exit.

### Step 5: Re-run Tests

After updating credentials, run:
```bash
python test_chitfund.py
```

You should now see:
```
✓ POST chitfund/ - Status: 201
✓ GET chitfund/X/ - Status: 200
✓ PUT chitfund/X/ - Status: 200
✓ DELETE chitfund/X/ - Status: 204
```

## Alternative: Use Existing User

If you have a user that you created through the frontend signup:

1. Add them to the Admin group:
```bash
python add_user_to_group.py
```

2. Follow the prompts to add your user to the Admin group

3. Update the test scripts with that user's email and password
