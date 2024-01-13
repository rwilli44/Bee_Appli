# Third-party imports
from django_filters import rest_framework as filters
from rest_framework import viewsets

# Local imports
from apiary.models import BeeYard, Hive
from .filters import BeeYardFilter, HiveFilter, PublicContactFilter
from .models import PublicContact
from .serializers import (
    BeeYardSerializerReadOnly,
    HiveSerializerReadOnly,
    PublicContactSerializerReadOnly,
)


##### Views for Public Access to Data via API #####


class BeeYardViewSet(viewsets.ModelViewSet):
    queryset = BeeYard.objects.all()
    serializer_class = BeeYardSerializerReadOnly
    filterset_class = BeeYardFilter
    filter_backends = (filters.DjangoFilterBackend,)


class HiveViewSet(viewsets.ModelViewSet):
    queryset = Hive.objects.all()
    serializer_class = HiveSerializerReadOnly
    filterset_class = HiveFilter
    filter_backends = (filters.DjangoFilterBackend,)


class BeekeeperViewSet(viewsets.ModelViewSet):
    queryset = PublicContact.objects.all()
    serializer_class = PublicContactSerializerReadOnly
    filterset_class = PublicContactFilter
    filter_backends = (filters.DjangoFilterBackend,)
