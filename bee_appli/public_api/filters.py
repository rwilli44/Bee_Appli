from django_filters import rest_framework as filters
from apiary.models import BeeYard, Hive
from .models import PublicContact
from django.db.models import Q


class HiveFilter(filters.FilterSet):
    """Filter for searching hives in the public API"""

    beeyard__beekeeper = filters.CharFilter(method="find_keeper")

    def find_keeper(self, queryset, name, value):
        # Exclude keepers who have not agreed to share their contact info
        queryset = queryset.exclude(beeyard__beekeeper__allows_public_contact=None)
        names = value.split()
        if len(names) == 1:
            filter_condition = Q(
                beeyard__beekeeper__first_name__icontains=names[0]
            ) | Q(beeyard__beekeeper__last_name__icontains=names[0])

        elif len(names) > 1:
            filter_condition = Q(
                beeyard__beekeeper__first_name__icontains=names[0]
            ) | Q(beeyard__beekeeper__last_name__icontains=names[1])
        queryset = queryset.filter(filter_condition)
        return queryset

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


class BeeYardFilter(filters.FilterSet):
    """Filter for searching beeyards in the public API"""

    beekeeper = filters.CharFilter(method="find_keeper")

    def find_keeper(self, queryset, name, value):
        # Exclude keepers who have not agreed to share their contact info
        queryset = queryset.exclude(beekeeper__allows_public_contact=None)
        names = value.split()
        if len(names) == 1:
            filter_condition = Q(beekeeper__first_name__icontains=names[0]) | Q(
                beekeeper__last_name__icontains=names[0]
            )

        elif len(names) > 1:
            filter_condition = Q(beekeeper__first_name__icontains=names[0]) | Q(
                beekeeper__last_name__icontains=names[1]
            )

        queryset = queryset.filter(filter_condition)

        return queryset

    class Meta:
        model = BeeYard
        fields = {
            "name": ["icontains", "contains", "exact"],
        }


class PublicContactFilter(filters.FilterSet):
    """Filter for seraching beekeeper contact information.
    in the public API. Only returns details of beeekeeper's
    who have agreed to make their information public."""

    first_name = filters.CharFilter(
        field_name="public_beekeeper_info__first_name", lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="public_beekeeper_info__last_name", lookup_expr="icontains"
    )
