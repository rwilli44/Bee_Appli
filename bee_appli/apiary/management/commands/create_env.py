# Standard library imports
import os
from pathlib import Path

# Third-party imports
from django.core.management.base import BaseCommand, CommandError
from django.core.management.utils import get_random_secret_key
from django.db import transaction


class Command(BaseCommand):
    help = """Createa .env with a new secret key for testing the Django TP project. 
    This command is to facilitate testing and grading the project. DB access data should
    never be included in this way in actual production code."""

    @transaction.atomic
    def handle(self, *args, **options):
        env_data = [
            "DB_ENGINE=django.db.backends.postgresql",
            "DB_NAME=test_db",
            "DB_USER=postgres",
            "DB_PASSWORD=postgres",
            "DB_HOST=localhost",
            "DB_PORT=5432",
            "SECRET_KEY=" + get_random_secret_key(),
        ]
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        env_path = os.path.join(BASE_DIR, ".env")
        with open(env_path, "w") as env_file:
            for item in env_data:
                env_file.write(item + "\n")
        print(
            """.env successfully created. 
        Verify that database and user info corresponds to your test system."""
        )
