from django.db import models
from django.db.models import CASCADE, SET_NULL
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Beekeeper(models.Model):
    first_name = models.CharField(max_length=100, help_text="Beekeeper's First Name")
    last_name = models.CharField(max_length=100, help_text="Beekeeper's Last Name")
    email = models.EmailField(max_length=100, help_text="Beekeeper's email address")
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="beekeeper"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BeeYard(models.Model):
    # add location later
    beekeeper = models.ForeignKey(
        # double check that cascade is the right thing to do here
        Beekeeper,
        on_delete=models.CASCADE,
        related_name="beeyards",
    )


class Hive(models.Model):
    ACTIVE = "active"
    PENDING = "pending"
    DESTROYED = "destroyed"

    HIVE_STATUS = [(ACTIVE, "Active"), (PENDING, "Pending"), (DESTROYED, "Destroyed")]

    status = models.CharField(choices=HIVE_STATUS, help_text="Status of the beehive")
    date_updated = models.DateField(
        auto_now=True, help_text="Date the status was updated"
    )
    beeyard = models.ForeignKey(BeeYard, on_delete=models.CASCADE, related_name="hives")
    queen_year = models.IntegerField()

    def __str__(self):
        return f"Hive {self.pk} in Bee Yard {self.beeyard.pk}"


class Intervention(models.Model):
    HARVEST = "Harvest"
    SRYUP_DISTRIBUTION = "Syrup Distribution"
    ARTIFICIAL_SWARMING = "Artificial Swarming"
    TREATMENT = "Treatment"
    DESTRUCTION_QUEEN_CELLS = "Destruction Queen Cells"
    HEALTH_CHECK = "Health Check"
    SUPER_INSTALLATION = "Super Installation"

    INTERVENTION_TYPES = (
        (HARVEST, "Harvest"),
        (SRYUP_DISTRIBUTION, "Syrup Distribution"),
        (ARTIFICIAL_SWARMING, "Artificial Swarming"),
        (TREATMENT, "Treatment"),
        (DESTRUCTION_QUEEN_CELLS, "Destruction Queen Cells"),
        (HEALTH_CHECK, "Health Check"),
        (SUPER_INSTALLATION, "Super Installation"),
    )

    intervention_type = models.CharField(
        choices=INTERVENTION_TYPES,
        help_text="The type of intervention from the given list",
    )
    date = models.DateTimeField(
        auto_now_add=True, help_text="The date of the intervention"
    )
    hive_affected = models.ForeignKey(
        Hive,
        on_delete=CASCADE,
        blank=False,
        help_text="The Hive concerned by the intervention",
    )
    limit = (
        models.Q(
            app_label="hive",
            model="quantity",
        )
        | models.Q(app_label="hive", model="artificialswarming")
        | models.Q(app_label="hive", model="treatment")
    )

    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to=limit,
    )
    object_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )


class Quantity(models.Model):
    KG = "Kilograms"
    ML = "Milliliters"
    UNIT_CHOICES = ((KG, "Kilograms"), (ML, "Milliliters"))
    quantity = models.FloatField(help_text="Quantity of the honey or syrup")
    units = models.CharField(
        choices=UNIT_CHOICES,
        help_text="The unit of measure for the honey or syrup",
    )

    def __str__(self):
        return f"{self.quantity} {self.units}"

    class Meta:
        verbose_name = "Quantity"


class ArtificialSwarming(models.Model):
    origin_hives = models.ManyToManyField(
        Hive, help_text="The parent Hives from which swarms were taken"
    )

    class Meta:
        verbose_name = "Artificial Swarming"


class Treatment(models.Model):
    treatment_type = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the treatment applied to the hive",
    )
    interventions = GenericRelation("Intervention")

    def __str__(self):
        return f"{self.treatment_type}"

    class Meta:
        verbose_name = "Treatment"


class Contamination(models.Model):
    PARASITE = "Parasite"
    ILLNESS = "Illness"

    TREATMENT_TYPES = (
        (PARASITE, "Parasite"),
        (ILLNESS, "Illness"),
    )

    type = models.CharField(
        choices=TREATMENT_TYPES,
        help_text="The type of contamination affecting the hive",
    )
    date = models.DateField(auto_now=True, help_text="Date the contamination was found")
    hive = models.ForeignKey(
        Hive, on_delete=models.CASCADE, related_name="contaminations"
    )
