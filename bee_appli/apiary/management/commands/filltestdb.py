# Standard library imports
import random

# Third-party imports
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Local imports
from apiary.models import (
    BeeYard,
    Contamination,
    Harvest,
    Hive,
    Intervention,
    SyrupDistribution,
    Treatment,
)
from public_api.models import PublicContact


class Command(BaseCommand):
    help = "Importing data for testing the Django TP project"

    @transaction.atomic
    def handle(self, *args, **options):
        # Create a superuser who can login to the admin panel
        admin_user = User.objects.create_user(username="admin", password="admin")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        # Constants to use for auto-creating objects
        USERS = [
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
        HIVE_NAMES = ["A", "B", "C", "D", "E"]
        SPECIES = [
            "Black bee",
            "Italian bee",
            "Caucasian bee",
            "Carnolian bee",
            "Buckfast bee",
        ]

        # List to store hives for adding interventions
        hives = []

        # Create users
        for user in USERS:
            first_name = user[0]
            last_name = user[1]
            username = first_name + last_name
            password = "Bees4ever!"
            email = first_name + last_name + "@testmail.com"
            new_user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email,
            )
            # Make some of the users contact information public. Keepers with D
            # in their name will not share contact information in the public API.
            if "d" not in username:
                PublicContact.objects.create(public_beekeeper_info=new_user)
            # Create a random number of beeyards
            numb_yards = random.randint(1, 4)
            for i in range(0, numb_yards):
                new_yard = BeeYard.objects.create(
                    name=username[2:6] + str(i), beekeeper=new_user
                )
                # Create a random number of hives and assign them a status
                numb_hives = random.randint(1, 5)
                for j in range(0, numb_hives):
                    if j == 3:
                        status = "destroyed"
                    elif j == 4:
                        status = "pending"
                    else:
                        status = "active"
                    new_hive = Hive.objects.create(
                        status=status,
                        species=SPECIES[i],
                        beeyard=new_yard,
                        queen_year=2020 + i % 3,
                        name=HIVE_NAMES[j],
                    )
                    # Save each hive to the hives list
                    hives.append(new_hive)

        # Create treatment interventions
        antifungal_treatment = Treatment.objects.create(treatment_type="antifungal")
        apivar_treatment = Treatment.objects.create(treatment_type="apivar")
        acide_treatment = Treatment.objects.create(treatment_type="oxalic_acid")
        # Apply the interventions to random hives
        for i in range(0, 6):
            hive = hives[random.randint(0, len(hives) - 1)]
            if i == 0 or i == 1:
                Contamination.objects.create(type="illness", hive=hive)
                Intervention.objects.create(
                    intervention_type="treatment",
                    hive_affected=hive,
                    content_object=antifungal_treatment,
                )
            elif i == 2 or i == 3:
                Contamination.objects.create(type="parasite", hive=hive)
                Intervention.objects.create(
                    intervention_type="treatment",
                    hive_affected=hive,
                    content_object=apivar_treatment,
                )
            else:
                Contamination.objects.create(type="parasite", hive=hive)
                Intervention.objects.create(
                    intervention_type="treatment",
                    hive_affected=hive,
                    content_object=acide_treatment,
                )

        # Create syrup distribution objects for random hives
        # Select a syrup at random
        quarter = len(hives) // 4
        for i in range(0, len(hives)):
            if i <= quarter:
                syrup_to_use = "nectar"
            elif quarter < i <= quarter * 2:
                syrup_to_use = "cane_sugar"
            elif quarter * 2 < i <= quarter * 3:
                syrup_to_use = "white_sugar"
            else:
                syrup_to_use = "raw_sugar"
            # Select a hive using the previous random number
            hive = hives[i]
            # Create the distribution object
            syrup = SyrupDistribution.objects.create(
                syrup_type=syrup_to_use,
                quantity=round(random.randint(1, 4) / 4, 2),
            )
            # Create the intervention object linked to the hive
            Intervention.objects.create(
                intervention_type="syrup_distribution",
                hive_affected=hive,
                content_object=syrup,
            )

        # Create harvests for each hive
        for hive in hives:
            # Create two harvests with a random amount of honey and
            # two health checks for each hive
            for i in range(0, 2):
                harvest = Harvest.objects.create(
                    quantity=round(random.randint(1, 5) / 7, 2)
                )
                # Create the intervention linking the harvest and hive
                Intervention.objects.create(
                    intervention_type="harvest",
                    hive_affected=hive,
                    content_object=harvest,
                )
                Intervention.objects.create(
                    intervention_type="health_check",
                    hive_affected=hive,
                )
            # Create a super installation for each hive
            Intervention.objects.create(
                intervention_type="super_installation",
                hive_affected=hive,
            )

            # Add another intervention to each hive choosing the type at random
            if random.randint(1, 10) % 3 == 0:
                Intervention.objects.create(
                    intervention_type="health_check",
                    hive_affected=hive,
                )
            elif random.randint(1, 10) % 5 == 0:
                Intervention.objects.create(
                    intervention_type="destruction_queen_cells",
                    hive_affected=hive,
                )
            else:
                # For artificial swarming, choose a child hive at random
                random_number = random.randint(0, len(hives) - 1)
                random_hive = hives[random_number]
                if random_hive == hive and random_number != 0:
                    random_hive = hives[random_number - 1]
                elif random_hive == hive:
                    random_hive = hives[1]
                # Create an artificial swarming intervention
                Intervention.objects.create(
                    intervention_type="artificial_swarming",
                    hive_affected=hive,
                    content_object=random_hive,
                )
        # Show in the terminal when the data is successfully imported
        self.stdout.write(self.style.SUCCESS("Data has been imported successfully"))
