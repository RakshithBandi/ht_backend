import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ht_backend.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("=== Checking Users in Database ===\n")

users = User.objects.all()
print(f"Total users: {users.count()}\n")

if users.count() > 0:
    print("Existing Users:")
    print("-" * 80)
    for user in users:
        groups = list(user.groups.values_list('name', flat=True))
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Groups: {groups}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Is Staff: {user.is_staff}")
        print("-" * 80)
else:
    print("No users found!")
    print("\nCreating admin user...")
    
    # Create Admin group if it doesn't exist
    admin_group, created = Group.objects.get_or_create(name='Admin')
    if created:
        print("Created Admin group")
    
    # Create admin user
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@ht.com',
        password='admin123',
        is_staff=True,
        is_superuser=True
    )
    admin_user.groups.add(admin_group)
    admin_user.save()
    
    print(f"✓ Created admin user:")
    print(f"  Email: admin@ht.com")
    print(f"  Password: admin123")
    print(f"  Groups: ['Admin']")
