# Third-party imports
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin

# Local imports
from .models import (
    BeeYard,
    Contamination,
    Hive,
    Intervention,
    Quantity,
    Treatment,
)


# Inline model to be displayed in Hive, Quantity and Treatment admins
class InterventionInline(GenericTabularInline):
    model = Intervention


class BeeYardAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name", "beekeeper", "hives")
    search_fields = ("name", "beekeeper", "hives")


admin.site.register(BeeYard, BeeYardAdmin)


class ContaminationAdmin(admin.ModelAdmin):
    list_display = ("type", "date", "hive")
    list_filter = ("type", "date", "hive")
    search_fields = ("type", "date", "hive")


admin.site.register(Contamination, ContaminationAdmin)


class HiveAdmin(admin.ModelAdmin):
    description = "test"
    inlines = [
        InterventionInline,
    ]
    GenericTabularInline.extra = 1

    list_display = ("status", "species", "date_updated", "beeyard", "queen_year")
    list_filter = ("status", "species", "date_updated", "beeyard", "queen_year")
    search_fields = ("status", "species", "date_updated", "beeyard", "queen_year")


admin.site.register(Hive, HiveAdmin)


class InterventionAdmin(admin.ModelAdmin):
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


admin.site.register(Intervention, InterventionAdmin)


class QuantityAdmin(admin.ModelAdmin):
    inlines = [
        InterventionInline,
    ]
    GenericTabularInline.extra = 1
    list_display = ("quantity", "units")
    list_filter = ("quantity", "units")
    search_fields = ("quantity", "units")


admin.site.register(Quantity, QuantityAdmin)


class TreatmentAdmin(admin.ModelAdmin):
    inlines = [
        InterventionInline,
    ]
    GenericTabularInline.extra = 1

    list_display = ("treatment_type",)
    list_filter = ("treatment_type", "interventions")
    search_fields = ("treatment_type", "interventions")


admin.site.register(Treatment, TreatmentAdmin)
