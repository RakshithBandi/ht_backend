import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ht_backend.settings')
django.setup()

from django.contrib.auth.models import User

print("\n=== Your Superuser Credentials ===\n")

superusers = User.objects.filter(is_superuser=True)

if superusers.count() == 0:
    print("No superuser found!")
else:
    for user in superusers:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Groups: {list(user.groups.values_list('name', flat=True))}")
        print()
        print("Update test_chitfund.py with:")
        print(f'ADMIN_EMAIL = "{user.email}"')
        print(f'ADMIN_PASSWORD = "your_password_here"')
        print()
        print("NOTE: The password is what YOU entered when creating the superuser.")
        print("If you forgot it, create a new superuser with: python manage.py createsuperuser")
