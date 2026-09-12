import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Creates the initial Django administrator from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_ADMIN_USERNAME")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")
        email = os.environ.get("DJANGO_ADMIN_EMAIL", "")

        if not username or not password:
            raise CommandError(
                "DJANGO_ADMIN_USERNAME and DJANGO_ADMIN_PASSWORD must both be set."
            )

        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        if user_model.objects.filter(**{username_field: username}).exists():
            self.stdout.write("Administrator already exists; skipping creation.")
            return

        user_model.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS("Administrator created."))
