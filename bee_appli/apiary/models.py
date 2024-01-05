from django.db import models
from django.db.models import CASCADE, SET_NULL
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class BeeYard(models.Model):
    # add location later
    name = models.CharField(
        max_length=100, help_text="A Name to Identify the Bee Yard Easily"
    )
    beekeeper = models.ForeignKey(
        # double check that cascade is the right thing to do here
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="beeyards",
    )

    def __str__(self):
        return f"{self.name} Bee Yard"


class Hive(models.Model):
    ACTIVE = "active"
    PENDING = "pending"
    DESTROYED = "destroyed"

    HIVE_STATUS = [(ACTIVE, "Active"), (PENDING, "Pending"), (DESTROYED, "Destroyed")]
    status = models.CharField(choices=HIVE_STATUS, help_text="Status of the beehive")
    BLACB = "Black bee"
    ITALB = "Italian bee"
    CAUCB = "Caucasian bee"
    CARNB = "Carnolian bee"
    BUCKB = "Buckfast bee"

    BEE_SPECIES = [
        (BLACB, "Black bee"),
        (ITALB, "Italian bee"),
        (CAUCB, "Caucasian bee"),
        (CARNB, "Carnolian bee"),
        (BUCKB, "Buckfast bee"),
    ]

    species = models.CharField(choices=BEE_SPECIES, help_text="Type of bees")

    date_updated = models.DateField(
        auto_now=True, help_text="Date the status was updated"
    )
    beeyard = models.ForeignKey(
        BeeYard, on_delete=models.SET_NULL, related_name="hives", null=True
    )
    queen_year = models.IntegerField()

    def __str__(self):
        return f"Hive {self.pk} in {self.beeyard.name} Bee Yard "

    class Meta:
        verbose_name = "Hive"


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
        help_text="The Hive concerned by the intervention. For Artificial Swarmings select the child hive.",
    )
    limit = (
        models.Q(app_label="apiary", model="quantity")
        | models.Q(app_label="apiary", model="hive")
        | models.Q(app_label="apiary", model="treatment")
    )

    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to=limit,
        help_text="""For interventions requiring a quantity (Harvest, Syrup) select Apiary | Quantity. 
        For an Artificial Swarming select Apiary | Hive to select the parent hive. 
        For a treatment, select Apiary | treatment to select the type of treatment. 
        Quantity and treatment objects must be created before they can be selected for an intervention.""",
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
        verbose_name_plural = "Quanitities"


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

    CONTAMINATION_TYPES = (
        (PARASITE, "Parasite"),
        (ILLNESS, "Illness"),
    )

    type = models.CharField(
        choices=CONTAMINATION_TYPES,
        help_text="The type of contamination affecting the hive",
    )
    date = models.DateField(auto_now=True, help_text="Date the contamination was found")
    hive = models.ForeignKey(
        Hive, on_delete=models.CASCADE, related_name="contaminations"
    )
