"""
Script to add an existing user to Admin or Manager group

Usage:
    python manage.py shell < add_user_to_group.py
"""

from django.contrib.auth.models import User, Group

# Configuration - CHANGE THESE VALUES
USER_EMAIL = 'htadmin@gmail.com'  # The email you're using to login
GROUP_NAME = 'Admin'  # Can be 'Admin' or 'Manager'

print("=" * 60)
print(f"Adding user to {GROUP_NAME} group")
print("=" * 60)

# Create group if it doesn't exist
group, created = Group.objects.get_or_create(name=GROUP_NAME)
if created:
    print(f"✓ Created '{GROUP_NAME}' group")
else:
    print(f"✓ '{GROUP_NAME}' group already exists")

# Find user by email
try:
    user = User.objects.get(email=USER_EMAIL)
    
    # Add user to group
    user.groups.add(group)
    
    print(f"\n✓ Successfully added user '{user.username}' ({USER_EMAIL}) to '{GROUP_NAME}' group")
    print(f"\nUser groups: {list(user.groups.values_list('name', flat=True))}")
    print("\n" + "=" * 60)
    print("Done! You can now login and add/edit/delete data.")
    print("=" * 60)
    
except User.DoesNotExist:
    print(f"\n✗ ERROR: User with email '{USER_EMAIL}' not found!")
    print("\nAvailable users:")
    for u in User.objects.all():
        print(f"  - {u.username} ({u.email})")
    print("\n" + "=" * 60)
