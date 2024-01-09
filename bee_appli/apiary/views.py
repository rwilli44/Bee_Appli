# Third-party imports
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters


# Local imports
from .models import BeeYard, Contamination, Hive, Intervention
from .localpermissions import IsKeeperOrReadOnly, IsKeeper
from .serializers import (
    BeeYardSerializer,
    ContaminationSerializer,
    HiveSerializer,
    InterventionSerializer,
)
from .filters import BeeYardFilter, ContaminationFilter, HiveFilter, InterventionFilter

##### Views for Beekeeper Access to Data via API #####


class BeeYardViewSet(viewsets.ModelViewSet):
    queryset = BeeYard.objects.all()
    serializer_class = BeeYardSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        # Only allows access to the beeyards of
        # the authenticated beekeeper
        IsKeeper,
    ]
    filterset_class = BeeYardFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self, *args, **kwargs):
        return BeeYard.objects.all().filter(beekeeper=self.request.user)

    @action(detail=False, methods=["GET"])
    def health_check_all_hives(self, request):
        print("Entering health_check_all_hives method")
        # ... other code
        print("Exiting health_check_all_hives method")

        return Response({"message": "Health check for all hives"})


class HiveViewSet(viewsets.ModelViewSet):
    queryset = Hive.objects.all()
    serializer_class = HiveSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        # Only allows access to the beeyards of
        # the authenticated beekeeper
        IsKeeper,
    ]
    filterset_class = HiveFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self, *args, **kwargs):
        return Hive.objects.all().filter(beeyard__beekeeper=self.request.user)


class InterventionViewSet(viewsets.ModelViewSet):
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        # Only allows access to the beeyards of
        # the authenticated beekeeper
        IsKeeper,
    ]
    filterset_class = InterventionFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self, *args, **kwargs):
        return Intervention.objects.all().filter(
            hive_affected__beeyard__beekeeper=self.request.user
        )


class ContaminationViewSet(viewsets.ModelViewSet):
    queryset = Contamination.objects.all()
    serializer_class = ContaminationSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        # Only allows access to the beeyards of
        # the authenticated beekeeper
        IsKeeper,
    ]
    filterset_class = ContaminationFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self, *args, **kwargs):
        return Contamination.objects.all().filter(
            hive__beeyard__beekeeper=self.request.user
        )


##### Template Views #####
def show_beeyards(request):
    """Returns a view of all the bee yards and hives of the connected user."""
    # If the user is not connected, return a 401 page
    if isinstance(request.user, AnonymousUser):
        return render(
            request,
            "401.html",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Query beeyards for those belonging to the user
    beeyard_query = BeeYard.objects.filter(beekeeper=request.user)

    # If none are found display a message
    if len(beeyard_query) == 0:
        return render(request, "index.html", {"beeyard_data": None})

    # For each beeyard, get data for each hive
    data = []
    for beeyard in beeyard_query.all():
        hive_query = Hive.objects.filter(beeyard=beeyard.id).all()
        hives = []
        for hive in hive_query:
            hives.append(hive.__dict__)
        data.append({"beeyard_name": beeyard.name, "hives": hives})

    # Create the json type object to pass the results to the template
    context = {"beeyard_data": data, "user": request.user.username}
    # test_context = {"beeyard_data": None, "user": "bob"}
    # Return an http response to the request with the filled-in template
    return render(request, "index.html", context)


def show_interventions(request):
    """Returns a view which shows all of the interventions for a given hive if
    it belongs to the connected user"""
    # If the user is not connected, return a 401 page
    if isinstance(request.user, AnonymousUser):
        return render(
            request,
            "401.html",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    # If no hive number is specified, return 404 error
    try:
        hive_id = request.GET["hive"]
    except:
        return render(
            request,
            "404.html",
            status=status.HTTP_404_NOT_FOUND,
        )
    # Query the given hive ID
    hive_query = Hive.objects.filter(id=hive_id).values()

    # If no hive is found, return not found page
    if len(hive_query) == 0:
        return render(
            request,
            "404.html",
            status=status.HTTP_404_NOT_FOUND,
        )
    # Verify that the hive belongs to the connected user
    beeyard_id = hive_query[0]["beeyard_id"]
    beeyard = BeeYard.objects.filter(id=beeyard_id).values()

    # If the hive doesn't belong to the user, return 401 page
    if beeyard[0]["beekeeper_id"] != request.user.id:
        return render(
            request,
            "401.html",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    # Query and return a view of the hive's interventions
    intervention_query = Intervention.objects.filter(hive_affected=hive_id).all()
    interventions = []
    hive = intervention_query[0].hive_affected
    for intervention in intervention_query:
        intervention_data = {
            "intervention_type": intervention.intervention_type,
            "date": intervention.date,
        }
        if intervention.intervention_type == "Syrup Distribution":
            intervention_data["quantity"] = intervention.content_object.quantity
            intervention_data["units"] = "liters"
            intervention_data["syrup_type"] = intervention.content_object.syrup_type
        elif intervention.intervention_type == "Harvest":
            intervention_data["quantity"] = intervention.content_object.quantity
            intervention_data["units"] = "kilos"
        elif intervention.intervention_type == "Treatement":
            intervention_data["type"] = intervention.content_object.type
        elif intervention.intervention_type == "Artificial Swarming":
            intervention_data["child_hive"] = intervention.content_object.__str__
        interventions.append(intervention_data)
    context = {"hive": hive.name, "interventions": interventions}
    return render(request, "interventions.html", context)
