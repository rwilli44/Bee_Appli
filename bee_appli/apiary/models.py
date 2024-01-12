# Standard library imports
import datetime

# Third-party imports
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CASCADE, SET_NULL
from django.core.validators import MaxValueValidator, MinValueValidator


class BeeYard(models.Model):
    """Model to store the details of a collection of hives in a specific location"""

    name = models.CharField(
        max_length=100, help_text="A Name to Identify the Bee Yard Easily"
    )

    beekeeper = models.ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        related_name="beeyards",
        help_text="The owner of the beeyard.",
    )

    def __str__(self):
        return f"{self.name} Bee Yard"


class Hive(models.Model):
    """Model to store the details of individual hives"""

    ACTIVE = "active"
    PENDING = "pending"
    DESTROYED = "destroyed"

    HIVE_STATUS = [(ACTIVE, "Active"), (PENDING, "Pending"), (DESTROYED, "Destroyed")]
    status = models.CharField(choices=HIVE_STATUS, help_text="Status of the beehive")

    # Unique identifiers that should remain CONSTANT
    BLACB = "black_bee"
    ITALB = "italian_bee"
    CAUCB = "caucasian_bee"
    CARNB = "carnolian_bee"
    BUCKB = "buckfast_bee"

    BEE_SPECIES = [
        (BLACB, "Black bee"),
        (ITALB, "Italian bee"),
        (CAUCB, "Caucasian bee"),
        (CARNB, "Carnolian bee"),
        (BUCKB, "Buckfast bee"),
    ]
    species = models.CharField(choices=BEE_SPECIES, help_text="Type of bees")
    name = models.CharField(
        max_length=100, help_text="A Name to Identify the Hive Easily"
    )
    date_updated = models.DateField(
        auto_now=True, help_text="Date the status was updated"
    )
    beeyard = models.ForeignKey(
        "BeeYard",
        on_delete=SET_NULL,
        related_name="hives",
        null=True,
        help_text="The beeyard where the hive is located.",
    )
    CURRENT_YEAR = datetime.date.today().year
    queen_year = models.IntegerField(
        default=CURRENT_YEAR,
        validators=[MinValueValidator(2000), MaxValueValidator(2040)],
        help_text="The year the queen bee was born.",
    )
    parent_hives = GenericRelation(
        "Intervention",
        help_text="Stores any parent hives in cases of artificial swarming.",
    )

    def __str__(self):
        return f"Hive {self.name} in {self.beeyard.name} Bee Yard "

    class Meta:
        # Necessary for showing properly in intervention admin
        verbose_name = "Hive"


class Intervention(models.Model):
    """Model to store the details of a interventions including artificial
    swarming, destruction of queen cells, harvesting honey, health checks,
    super installation, syrup distribution, and treatments. Uses a generic
    foreign key for interventions which require more details."""

    # Unique identifiers that should remain CONSTANT
    ARTIFICIAL_SWARMING = "artificial_swarming"
    DESTRUCTION_QUEEN_CELLS = "destruction_queen_cells"
    HARVEST = "harvest"
    HEALTH_CHECK = "health_check"
    SUPER_INSTALLATION = "super_installation"
    SYRUP_DISTRIBUTION = "syrup_distribution"
    TREATMENT = "treatment"

    INTERVENTION_TYPES = (
        (ARTIFICIAL_SWARMING, "Artificial Swarming"),
        (DESTRUCTION_QUEEN_CELLS, "Destruction Queen Cells"),
        (HARVEST, "Harvest"),
        (HEALTH_CHECK, "Health Check"),
        (SUPER_INSTALLATION, "Super Installation"),
        (SYRUP_DISTRIBUTION, "Syrup Distribution"),
        (TREATMENT, "Treatment"),
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
        help_text="The Hive concerned by the intervention. For Artificial Swarmings select the PARENT hive.",
    )
    # Queries to determine which objects may be selected as the generic foreign key
    limit = (
        models.Q(app_label="apiary", model="harvest")
        | models.Q(app_label="apiary", model="hive")
        | models.Q(app_label="apiary", model="syrupdistribution")
        | models.Q(app_label="apiary", model="treatment")
    )
    # Field to select one of the above object choices, null if not needed
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to=limit,
        help_text="""For an Artificial Swarming select Apiary | Hive to select the CHILD hive. 
        For a treatment, select Apiary | Treatment to select the type of treatment. 
        Harvest and Syrup Distribution objects must be created before they can be selected for an intervention.""",
    )
    # The ID of the foreign key object, null if no FK is needed
    object_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="The ID of the FK object needed to complete the intervention information..",
    )
    # The Generic Foreign Key which can refer to a hive (artificial swarming),
    # quantity, or treatment if the intervention type requires this information
    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )


class Harvest(models.Model):
    """Model to store quantities of honey harvested. Linked to specific
    interventions via a generic foreign key relationship."""

    quantity = models.FloatField(help_text="Quantity of the honey harvested in kilos")

    def __str__(self):
        return f"{self.quantity} kilograms"

    class Meta:
        # Necessary for showing properly in intervention admin
        verbose_name = "Harvest"


class SyrupDistribution(models.Model):
    """Model to store quantities  and types of syrup distributed. Linked to
    specific interventions via a generic foreign key relationship."""

    # Unique identifiers that should remain CONSTANT
    NECTAR = "nectar"
    CANE_SUGAR = "cane_sugar"
    WHITE_SUGAR = "white_sugar"
    RAW_SUGAR = "raw_sugar"

    SYRUP_TYPES = (
        (NECTAR, "nectar"),
        (CANE_SUGAR, "cane_sugar"),
        (WHITE_SUGAR, "white_sugar"),
        (RAW_SUGAR, "raw_sugar"),
    )
    syrup_type = models.CharField(
        choices=SYRUP_TYPES,
        help_text="The type of syrup provided to the hive",
    )
    quantity = models.FloatField(help_text="Quantity of the syrup provided in liters")

    def __str__(self):
        return f"{self.quantity} liters"

    class Meta:
        # Necessary for showing properly in intervention admin
        verbose_name = "Syrup Distribution"


class Treatment(models.Model):
    """Model to store details of treatment interventions which links
    to the Intervention model via a generic foreign key relationship."""

    # Unique identifiers that should remain CONSTANT
    ANTIFUNGAL = "antifungal"
    APIVAR = "apivar"
    ACIDE = "oxalic_acid"

    TREATMENTS = (
        (ANTIFUNGAL, "Antifungal"),
        (APIVAR, "Apivar"),
        (ACIDE, "Oxalic Acid"),
    )
    treatment_type = models.CharField(
        choices=TREATMENTS,
        unique=True,
        help_text="Name of the treatment applied to the hive",
    )
    interventions = GenericRelation("Intervention")

    def __str__(self):
        return f"{self.treatment_type}"

    class Meta:
        # Necessary for showing properly in intervention admin
        verbose_name = "Treatment"


class Contamination(models.Model):
    """A model to store data about hive contaminations."""

    # Unique identifiers that should remain CONSTANT
    PARASITE = "parasite"
    ILLNESS = "illness"

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
        Hive,
        on_delete=models.CASCADE,
        related_name="contaminations",
        help_text="The infected hive.",
    )
