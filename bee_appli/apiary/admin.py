# Third-party imports
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

# Local imports
from .models import (
    BeeYard,
    Contamination,
    Hive,
    Intervention,
    Harvest,
    SyrupDistribution,
    Treatment,
)


# Inline model to be displayed in Hive, Quantity and Treatment admins
class InterventionInline(GenericTabularInline):
    model = Intervention

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        # Check the parent admin model
        parent_model = self.parent_model

        # Customize default values based on the parent model
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


class HarvestAdmin(admin.ModelAdmin):
    inlines = [
        InterventionInline,
    ]
    GenericTabularInline.extra = 1
    list_display = ("quantity",)
    list_filter = ("quantity",)
    search_fields = ("quantity",)


admin.site.register(Harvest, HarvestAdmin)


class SyrupDistributionAdmin(admin.ModelAdmin):
    inlines = [
        InterventionInline,
    ]
    GenericTabularInline.extra = 1
    list_display = ("quantity", "syrup_type")
    list_filter = ("quantity", "syrup_type")
    search_fields = ("quantity", "syrup_type")


admin.site.register(SyrupDistribution, SyrupDistributionAdmin)


class TreatmentAdmin(admin.ModelAdmin):
    inlines = [
        InterventionInline,
    ]
    GenericTabularInline.extra = 1

    list_display = ("treatment_type",)
    list_filter = ("treatment_type", "interventions")
    search_fields = ("treatment_type", "interventions")


admin.site.register(Treatment, TreatmentAdmin)
