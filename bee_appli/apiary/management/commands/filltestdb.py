from django.core.management.base import BaseCommand, CommandError
from apiary.models import BeeYard, Hive, Intervention, Quantity
from django.contrib.auth.models import User

from django.db import transaction


class Command(BaseCommand):
    help = "Importing data for solo project"

    @transaction.atomic
    def handle(self, *args, **options):
        # user1 = User.objects.create(
        #     username="SpookyCat",
        #     password="Loves2kill",
        #     first_name="Spooky",
        #     last_name="Cat",
        #     email="cat@aol.com",
        # )

        # yard1 = BeeYard.objects.create(name="Boo", beekeeper=user1)
        # hive1 = Hive.objects.create(
        #     status="active", species="Black bee", beeyard=yard1, queen_year=2022
        # )
        # quantity = Quantity.objects.create(quantity=15, units="Kilograms")
        # Intervention.objects.create(intervention_type="Harvest", hive_affected=hive1, content_type="")
        # self.stdout.write(self.style.SUCCESS("Data has been imported successfully"))
        pass
