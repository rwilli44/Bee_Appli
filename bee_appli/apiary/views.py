# Third-party imports
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from rest_framework import permissions, status, viewsets

# Local imports
from .models import BeeYard, Hive, Intervention
from .serializers import BeeYardSerializer, HiveSerializer, InterventionSerializer
from .localpermissions import IsKeeperOrReadOnly


##### Views for Beekeeper Access to Data via API #####


class BeeYardViewSet(viewsets.ModelViewSet):
    queryset = BeeYard.objects.all()
    serializer_class = BeeYardSerializer
    permission_classes = [permissions.IsAuthenticated, IsKeeperOrReadOnly]


class HiveViewSet(viewsets.ModelViewSet):
    queryset = Hive.objects.all()
    serializer_class = HiveSerializer
    permission_classes = [permissions.IsAuthenticated, IsKeeperOrReadOnly]


class InterventionViewSet(viewsets.ModelViewSet):
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer
    permission_classes = [permissions.IsAuthenticated, IsKeeperOrReadOnly]


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
    beeyard_query = BeeYard.objects.filter(beekeeper=request.user).values()

    # If none are found display a message
    if len(beeyard_query) == 0:
        return render(request, "index.html", {"beeyard_data": None})

    # For each beeyard, get data for each hive
    data = []
    for beeyard in beeyard_query:
        hive_query = Hive.objects.filter(beeyard=beeyard["id"]).values()
        beeyard_data = BeeYardSerializer(beeyard).data
        hive_data = HiveSerializer(hive_query, many=True).data
        data.append({"beeyard_name": beeyard_data["name"], "hives": hive_data})

    # Create the json type object to pass the results to the template
    context = {"beeyard_data": data, "user": request.user.username}

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
    intervention_query = Intervention.objects.filter(hive_affected=hive_id).values()
    interventions = InterventionSerializer(intervention_query, many=True).data
    context = {"hive": hive_id, "interventions": interventions}
    return render(request, "interventions.html", context)
