from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Assign roles to users'

    def handle(self, *args, **kwargs):
        # Create groups if they don't exist
        admin_group, created = Group.objects.get_or_create(name='Admin')
        user_group, created = Group.objects.get_or_create(name='User')

        # Assign users to groups
        try:
            admin_user = User.objects.get(username='admin')  # Replace with actual username
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {admin_user.username} to Admin group.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User admin_user does not exist.'))

        # You can add more users similarly
        try:
            regular_user = User.objects.get(username='user0')  # Replace with actual username
            regular_user.groups.add(user_group)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {regular_user.username} to User group.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User regular_user does not exist.'))
