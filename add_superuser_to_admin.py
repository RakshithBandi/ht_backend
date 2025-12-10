import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ht_backend.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("=== Adding Superuser to Admin Group ===\n")

# Get or create Admin group
admin_group, created = Group.objects.get_or_create(name='Admin')
if created:
    print("✓ Created Admin group\n")
else:
    print("✓ Admin group already exists\n")

# Get all superusers
superusers = User.objects.filter(is_superuser=True)

if superusers.count() == 0:
    print("✗ No superusers found!")
    print("Please run: python manage.py createsuperuser")
else:
    print(f"Found {superusers.count()} superuser(s):\n")
    
    for user in superusers:
        # Add to Admin group if not already in it
        if not user.groups.filter(name='Admin').exists():
            user.groups.add(admin_group)
            user.save()
            print(f"✓ Added '{user.username}' to Admin group")
        else:
            print(f"✓ '{user.username}' already in Admin group")
        
        print(f"  Email: {user.email}")
        print(f"  Username: {user.username}")
        print(f"  Groups: {list(user.groups.values_list('name', flat=True))}")
        print()
    
    print("\n=== Next Steps ===")
    print("\n1. Update test_chitfund.py (lines 10-11):")
    first_user = superusers.first()
    print(f"   ADMIN_EMAIL = \"{first_user.email}\"")
    print(f"   ADMIN_PASSWORD = \"your_password\"  # The password you just created")
    
    print("\n2. Update test_http_methods.py (lines 20-21):")
    print(f"   ADMIN_EMAIL = \"{first_user.email}\"")
    print(f"   ADMIN_PASSWORD = \"your_password\"  # The password you just created")
    
    print("\n3. Run the tests:")
    print("   python test_chitfund.py")
