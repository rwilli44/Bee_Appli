from django.contrib import admin
from .models import (
    Beekeeper,
    BeeYard,
    Contamination,
    Hive,
    Intervention,
    Quantity,
    Treatment,
)


class BeekeeperAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "user",
    )
    list_filter = ("first_name", "last_name", "beeyards")
    search_fields = ("first_name", "last_name", "beeyards")


admin.site.register(Beekeeper, BeekeeperAdmin)


class BeeYardAdmin(admin.ModelAdmin):
    list_filter = ("beekeeper", "hives")
    search_fields = ("beekeeper", "hives")


admin.site.register(BeeYard, BeeYardAdmin)


class ContaminationAdmin(admin.ModelAdmin):
    list_display = ("type", "date", "hive")
    list_filter = ("type", "date", "hive")
    search_fields = ("type", "date", "hive")


admin.site.register(Contamination, ContaminationAdmin)


class HiveAdmin(admin.ModelAdmin):
    list_display = ("status", "date_updated", "beeyard", "queen_year")
    list_filter = ("status", "date_updated", "beeyard", "queen_year")
    search_fields = ("status", "date_updated", "beeyard", "queen_year")


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
    list_display = ("quantity", "units")
    list_filter = ("quantity", "units")
    search_fields = ("quantity", "units")


admin.site.register(Quantity, QuantityAdmin)


class TreatmentAdmin(admin.ModelAdmin):
    list_display = ("treatment_type",)
    list_filter = ("treatment_type", "interventions")
    search_fields = ("treatment_type", "interventions")


admin.site.register(Treatment, TreatmentAdmin)
