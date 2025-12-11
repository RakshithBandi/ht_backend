import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ht_backend.settings")
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    username = 'htuser'
    email = 'htuser@gmail.com'
    password = 'htportal@123'
    
    try:
        if not User.objects.filter(username=username).exists():
            print(f"Creating superuser: {username}")
            User.objects.create_superuser(username, email, password)
            print("Superuser created successfully.")
        else:
            print(f"Superuser {username} already exists.")
    except Exception as e:
        print(f"Error creating superuser: {e}")

if __name__ == '__main__':
    create_superuser()
