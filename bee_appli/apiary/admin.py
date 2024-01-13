# Third-party imports
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

# Local imports
from .models import (
    BeeYard,
    Contamination,
    Harvest,
    Hive,
    Intervention,
    SyrupDistribution,
    Treatment,
)

admin.site.site_header = "Bee Appli by Rachel WILLIAMS"


class InterventionInline(GenericTabularInline):
    """Class for displaying inline models of interventions in the Hive,
    Quantity and Treatment admins"""

    model = Intervention

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        # Check the parent admin model
        parent_model = self.parent_model

        # Customize default values for the intervention type based on the parent model
        if parent_model == Harvest:
            formset.form.base_fields["intervention_type"].initial = "Harvest"
        elif parent_model == SyrupDistribution:
            formset.form.base_fields["intervention_type"].initial = "Syrup Distribution"
        elif parent_model == Treatment:
            formset.form.base_fields["intervention_type"].initial = "Treatment"
        elif parent_model == Hive:
            formset.form.base_fields[
                "intervention_type"
            ].initial = "Artificial Swarming"

        return formset


class BeeYardAdmin(admin.ModelAdmin):
    """Admin model for displaying bee yard data."""

    list_display = ("name",)
    list_filter = ("name", "beekeeper", "hives")
    search_fields = ("name", "beekeeper", "hives")
    list_per_page = 25


admin.site.register(BeeYard, BeeYardAdmin)


class ContaminationAdmin(admin.ModelAdmin):
    """Admin model for displaying contamination data."""

    list_display = ("type", "date", "hive")
    list_filter = ("type", "date", "hive")
    search_fields = ("type", "date", "hive")
    list_per_page = 25


admin.site.register(Contamination, ContaminationAdmin)


class HiveAdmin(admin.ModelAdmin):
    """Admin model for displaying hive data."""

    inlines = [
        InterventionInline,
    ]
    # Set default to showing only one inline row to add data
    GenericTabularInline.extra = 1

    list_display = ("status", "species", "date_updated", "beeyard", "queen_year")
    list_filter = ("status", "species", "date_updated", "beeyard", "queen_year")
    search_fields = ("status", "species", "date_updated", "beeyard", "queen_year")
    list_per_page = 25


admin.site.register(Hive, HiveAdmin)


class InterventionAdmin(admin.ModelAdmin):
    """Admin model for displaying intervention data."""

    list_display = (
        "intervention_type",
        "date",
        "hive_affected",
        "content_type",
        "object_id",
        "content_object",
    )
    list_filter = (
        "intervention_type",
        "date",
        "hive_affected",
        "content_type",
        "object_id",
    )
    search_fields = (
        "intervention_type",
        "date",
        "hive_affected",
        "content_type",
        "object_id",
    )
    list_per_page = 25


admin.site.register(Intervention, InterventionAdmin)


class HarvestAdmin(admin.ModelAdmin):
    """Admin model for displaying harvest data."""

    # Add possibility to edit/add an intervention from harvest admin
    inlines = [
        InterventionInline,
    ]
    # Set default to one row intervention data to add
    GenericTabularInline.extra = 1

    list_display = ("quantity",)
    list_filter = ("quantity",)
    search_fields = ("quantity",)
    list_per_page = 25


admin.site.register(Harvest, HarvestAdmin)


class SyrupDistributionAdmin(admin.ModelAdmin):
    """Admin model for displaying syrup distribution data."""

    # Add possibility to edit/add an intervention from syrup distr. admin
    inlines = [
        InterventionInline,
    ]
    # Set default to one row intervention data to add
    GenericTabularInline.extra = 1
    list_display = ("quantity", "syrup_type")
    list_filter = ("quantity", "syrup_type")
    search_fields = ("quantity", "syrup_type")
    list_per_page = 25


admin.site.register(SyrupDistribution, SyrupDistributionAdmin)


class TreatmentAdmin(admin.ModelAdmin):
    """Admin model for displaying treatment data."""

    # Add possibility to edit/add an intervention from treatment admin
    inlines = [
        InterventionInline,
    ]
    # Set default to one row intervention data to add
    GenericTabularInline.extra = 1

    list_display = ("treatment_type",)
    list_filter = ("treatment_type", "interventions")
    search_fields = ("treatment_type", "interventions")
    list_per_page = 25


admin.site.register(Treatment, TreatmentAdmin)
