from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Creates HT admin and manager users'

    def handle(self, *args, **kwargs):
        self.stdout.write("=" * 60)
        self.stdout.write("Setting up HT Admin and Manager Users")
        self.stdout.write("=" * 60)

        # Create groups
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS("✓ Created 'Admin' group"))
        else:
            self.stdout.write("✓ 'Admin' group already exists")

        manager_group, created = Group.objects.get_or_create(name='Manager')
        if created:
            self.stdout.write(self.style.SUCCESS("✓ Created 'Manager' group"))
        else:
            self.stdout.write("✓ 'Manager' group already exists")

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("Creating/Updating Users")
        self.stdout.write("=" * 60)

        # HT Admin User
        admin_email = 'htadmin@gmail.com'
        admin_password = 'ekadanthaHT'

        try:
            admin_user = User.objects.get(email=admin_email)
            self.stdout.write(f"✓ User '{admin_user.username}' already exists")
        except User.DoesNotExist:
            admin_user = User.objects.create_user(
                username='htadmin',
                email=admin_email,
                password=admin_password,
                first_name='HT',
                last_name='Admin'
            )
            self.stdout.write(self.style.SUCCESS(f"✓ Created user 'htadmin'"))

        # Always update password to ensure it's correct
        admin_user.set_password(admin_password)
        admin_user.save()
        
        # Add to Admin group
        admin_user.groups.clear()
        admin_user.groups.add(admin_group)
        self.stdout.write(f"  Email: {admin_email}")
        self.stdout.write(f"  Password: {admin_password}")
        self.stdout.write(self.style.SUCCESS(f"  Groups: Admin"))

        # HT Manager User
        manager_email = 'htmanager@gmail.com'
        manager_password = 'vinayakaHT'

        try:
            manager_user = User.objects.get(email=manager_email)
            self.stdout.write(f"\n✓ User '{manager_user.username}' already exists")
        except User.DoesNotExist:
            manager_user = User.objects.create_user(
                username='htmanager',
                email=manager_email,
                password=manager_password,
                first_name='HT',
                last_name='Manager'
            )
            self.stdout.write(self.style.SUCCESS(f"\n✓ Created user 'htmanager'"))

        # Always update password to ensure it's correct
        manager_user.set_password(manager_password)
        manager_user.save()
        
        # Add to Manager group
        manager_user.groups.clear()
        manager_user.groups.add(manager_group)
        self.stdout.write(f"  Email: {manager_email}")
        self.stdout.write(f"  Password: {manager_password}")
        self.stdout.write(self.style.SUCCESS(f"  Groups: Manager"))

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("Setup Complete!"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"\nYou can now login with:")
        self.stdout.write(f"\n1. HT Admin:")
        self.stdout.write(f"   Email: {admin_email}")
        self.stdout.write(f"   Password: {admin_password}")
        self.stdout.write(f"\n2. HT Manager:")
        self.stdout.write(f"   Email: {manager_email}")
        self.stdout.write(f"   Password: {manager_password}")
        self.stdout.write("\n" + "=" * 60)
