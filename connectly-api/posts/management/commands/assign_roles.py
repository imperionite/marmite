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
            admin_user = User.objects.get(username='admin')
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {admin_user.username} to Admin group.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User admin does not exist.'))

        try:
            admin_user0 = User.objects.get(username='user0')
            admin_user0.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {admin_user0.username} to Admin group.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User user0 does not exist.'))

        # Assign all other users to the User group
        other_users = User.objects.exclude(username__in=['admin', 'user0'])
        for user in other_users:
            try:
                user.groups.add(user_group)
                self.stdout.write(self.style.SUCCESS(f'Successfully added {user.username} to User group.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to add {user.username} to User group: {e}'))