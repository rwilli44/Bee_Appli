from django.core.management.base import BaseCommand, CommandError
from apiary.models import BeeYard, Hive, Intervention, Harvest
from public_api.models import PublicContact
from django.contrib.auth.models import User

from django.db import transaction
import random


class Command(BaseCommand):
    help = "Importing data for solo project"

    @transaction.atomic
    def handle(self, *args, **options):
        users = [
            ("Idgie", "Threadgood"),
            ("Frank", "Wang"),
            ("Alice", "Taylor"),
            ("Ivy", "Clark"),
            ("David", "Lee"),
            ("Eva", "Aldridge"),
            ("Grace", "Johnson"),
            ("Henry", "Garcia"),
            ("Charlie", "Brown"),
            ("Jodie", "Taylor"),
        ]
        hive_names = ["A", "B", "C", "D"]
        species = [
            "Black bee",
            "Italian bee",
            "Caucasian bee",
            "Carnolian bee",
            "Buckfast bee",
        ]
        for user in users:
            first_name = user[0]
            last_name = user[1]
            username = first_name + last_name
            password = "Bees4ever!"
            email = first_name + last_name + "@testmail.com"
            numb_yards = random.randint(1, 5)
            new_user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email,
            )
            if "r" in username:
                PublicContact.objects.create(public_beekeeper_info=new_user)
            for i in range(0, numb_yards):
                new_yard = BeeYard.objects.create(
                    name=username[2:6] + str(i), beekeeper=new_user
                )
                numb_hives = random.randint(1, 4)
                for j in range(0, numb_hives):
                    if j == 3:
                        status = "destroyed"
                    elif j == 4:
                        status = "pending"
                    else:
                        status = "active"
                    Hive.objects.create(
                        status=status,
                        species=species[i],
                        beeyard=new_yard,
                        queen_year=2020 + i % 3,
                        name=hive_names[j],
                    )

        # yard1 = BeeYard.objects.create(name="Boo", beekeeper=user1)
        # hive1 = Hive.objects.create(
        #     status="active", species="Black bee", beeyard=yard1, queen_year=2022
        # )
        # quantity = Quantity.objects.create(quantity=15, units="Kilograms")
        # Intervention.objects.create(intervention_type="Harvest", hive_affected=hive1, content_type="")
        self.stdout.write(self.style.SUCCESS("Data has been imported successfully"))
