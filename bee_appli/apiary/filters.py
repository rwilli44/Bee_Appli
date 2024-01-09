from django_filters import rest_framework as filters
from .models import (
    BeeYard,
    Hive,
    Harvest,
    Intervention,
    SyrupDistribution,
    Treatment,
    Contamination,
)
from django.db.models import Q


class ContaminationFilter(filters.FilterSet):
    """Class for a beekeper to filter their contaminations"""

    # addhive
    class Meta:
        model = Contamination
        fields = {
            "type": ["icontains", "contains", "exact"],
            "date": ["exact", "gt", "lt", "gte", "lte"],
        }


class BeeYardFilter(filters.FilterSet):
    """Class for a beekeeper to filter their beeyards"""

    class Meta:
        model = BeeYard
        fields = {
            "name": ["icontains", "contains", "exact"],
        }


class HiveFilter(filters.FilterSet):
    class Meta:
        model = Hive
        fields = {
            "name": ["icontains", "contains", "exact"],
            "status": ["icontains", "contains", "exact"],
            "species": ["icontains", "contains", "exact"],
            "date_updated": ["exact", "gt", "lt", "gte", "lte"],
            "beeyard__name": ["icontains", "contains", "exact"],
            "beeyard__id": ["exact"],
            "queen_year": ["exact", "gt", "lt", "gte", "lte"],
        }


class InterventionFilter(filters.FilterSet):
    treatment_type = filters.CharFilter(method="find_treatment_type")

    def find_treatment_type(self, queryset, name, value):
        matching_interventions = []
        for result in queryset:
            if hasattr(result.content_object, "treatment_type"):
                matching_interventions.append(result.object_id)
        treatment_query = Treatment.objects.filter(pk__in=matching_interventions)
        treatment_query = treatment_query.filter(treatment_type__icontains=value)
        treatment_matches = []
        for treatment in treatment_query:
            treatment_matches.append(treatment.id)
        queryset = queryset.filter(object_id__in=treatment_matches)

        return queryset

    syrup_type = filters.CharFilter(method="find_syrup_type")

    def find_syrup_type(self, queryset, name, value):
        matching_interventions = []
        for result in queryset:
            if hasattr(result.content_object, "syrup_type"):
                matching_interventions.append(result.object_id)
        syrup_query = SyrupDistribution.objects.filter(pk__in=matching_interventions)
        syrup_query = syrup_query.filter(syrup_type__icontains=value)
        syrup_matches = []
        for syrup in syrup_query:
            syrup_matches.append(syrup.id)
        queryset = queryset.filter(object_id__in=syrup_matches)

        return queryset

    harvest_lt = filters.CharFilter(method="find_harvest_lt")

    def find_harvest_lt(self, queryset, name, value):
        matching_interventions = []
        for result in queryset:
            if hasattr(result.content_object, "quantity") and isinstance(
                result.content_object, Harvest
            ):
                matching_interventions.append(result.object_id)
        harvest_query = Harvest.objects.filter(pk__in=matching_interventions)
        harvest_query = harvest_query.filter(quantity__lt=value)
        harvest_matches = []
        for harvest in harvest_query:
            harvest_matches.append(harvest.id)
        queryset = queryset.filter(object_id__in=harvest_matches)

        return queryset

    harvest_gt = filters.CharFilter(method="find_harvest_gt")

    def find_harvest_gt(self, queryset, name, value):
        matching_interventions = []
        for result in queryset:
            if hasattr(result.content_object, "quantity") and isinstance(
                result.content_object, Harvest
            ):
                matching_interventions.append(result.object_id)
        harvest_query = Harvest.objects.filter(pk__in=matching_interventions)
        harvest_query = harvest_query.filter(quantity__gt=value)
        harvest_matches = []
        for harvest in harvest_query:
            harvest_matches.append(harvest.id)
        queryset = queryset.filter(object_id__in=harvest_matches)

        return queryset

    class Meta:
        model = Intervention
        fields = {
            "intervention_type": ["icontains", "contains", "exact"],
            "date": ["exact", "gt", "lt", "gte", "lte"],
            "hive_affected__id": ["exact"],
            "hive_affected__beeyard_id": ["exact"],
            "object_id": ["exact"],
        }
