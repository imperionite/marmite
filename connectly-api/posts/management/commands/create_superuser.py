from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser from environment variables'

    def handle(self, *args, **kwargs):
        username = config('SU_USERNAME')
        email = config('SU_EMAIL')
        password = config('SU_PASSWORD')

        if not username or not email or not password:
            self.stdout.write(self.style.ERROR('Missing environment variables for superuser.'))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password, is_staff=True, is_active=True, is_superuser=True)
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser {username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} already exists.'))

