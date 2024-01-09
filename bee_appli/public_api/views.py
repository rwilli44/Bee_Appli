# Third-party imports
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import views
from rest_framework.reverse import reverse

# Local imports
from apiary.models import BeeYard, Hive
from .filters import BeeYardFilter, HiveFilter, PublicContactFilter
from .models import PublicContact
from .serializers import (
    BeeYardSerializerReadOnly,
    HiveSerializerReadOnly,
    PublicContactSerializer,
)


##### Views for Beekeeper Access to Data via API #####


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
    serializer_class = PublicContactSerializer
    filterset_class = PublicContactFilter
    filter_backends = (filters.DjangoFilterBackend,)


##### Custom View for the Public API #####


class PublicAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "message": "Public API - Read Only",
            "endpoints": {
                "beeyards": reverse("beeyards-list", request=request),
                "hives": reverse("hives-list", request=request),
                "beekeepers": reverse("beekeepers-list", request=request),
            },
        }
        return Response(data)
