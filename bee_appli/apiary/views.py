# Third-party imports
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django_filters import rest_framework as filters
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


# Local imports
from .models import BeeYard, Contamination, Hive, Intervention
from .permissions import IsKeeper
from .serializers import (
    BeeYardSerializer,
    ContaminationSerializer,
    HiveSerializer,
    InterventionSerializer,
)
from .filters import BeeYardFilter, ContaminationFilter, HiveFilter, InterventionFilter


# custom 404 view
def custom_404(request, exception):
    return render(request, "/templates/404.html", status=404)


# custom 401 view
def custom_401(request, exception):
    return render(request, "/templates/401.html", status=401)


##### Views for Beekeeper Access to Data via private API #####


class BeeYardViewSet(viewsets.ModelViewSet):
    """API to allow CRUD on beeyard data."""

    # Set the queryset to all beeyard objects
    queryset = BeeYard.objects.all()
    serializer_class = BeeYardSerializer
    permission_classes = [
        # Only allow access to the beeyards of
        # the authenticated beekeeper
        permissions.IsAuthenticated,
        # Only show data for the current user
        IsKeeper,
    ]
    filterset_class = BeeYardFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self, *args, **kwargs):
        """Restricts the queryset to only items owned by the requesting user."""
        return BeeYard.objects.all().filter(beekeeper=self.request.user)

    @action(detail=True, methods=["POST"])
    def health_check_all_hives(self, request, pk):
        """Function to apply a health check to all the hives in the same beeyard."""
        # Get the beeyard object for the provided ID
        beeyard = BeeYard.objects.get(id=pk)
        # Find hives which belong to the beeyard
        hives = Hive.objects.filter(beeyard=beeyard)
        # Save a copy of the intervention object for the HTTP response
        interventions = []
        # Make an intervention object for each hive and add it to the response data
        for hive in hives:
            intervention = Intervention.objects.create(
                intervention_type="Health Check", hive_affected=hive
            )
            intervention = InterventionSerializer(intervention)
            interventions.append(intervention.data)
        # Put the expected JSON format.
        response_data = {"interventions": interventions}
        # Return the created data and a 201 Created code
        return Response(response_data, status=status.HTTP_201_CREATED)


class HiveViewSet(viewsets.ModelViewSet):
    """View to allow CRUD operations on hive data."""

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
        """Restricts the queryset to only hives belonging to the connected beekeeper."""
        return Hive.objects.all().filter(beeyard__beekeeper=self.request.user)


class InterventionViewSet(viewsets.ModelViewSet):
    """View to allow CRUD operations on intervention data."""

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
        """Restricts the queryset to only interventions on hives
        belonging to the connected beekeeper."""

        return Intervention.objects.all().filter(
            hive_affected__beeyard__beekeeper=self.request.user
        )


class ContaminationViewSet(viewsets.ModelViewSet):
    """View to allow CRUD operations on hive data."""

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
        """Restricts the queryset to only hives belonging to the connected beekeeper."""
        return Contamination.objects.all().filter(
            hive__beeyard__beekeeper=self.request.user
        )


##### Template Views #####
class LoginInterfaceView(LoginView):
    """Login view used to test axes, does not lead the user anywhere yet"""

    template_name = "login.html"


def logout_request(request):
    """Sends a confirmation message and redirects on logout."""
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/apiary/login")


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
        # Doesn't seem to be working, goal was to show the details but no time to debug
        if intervention.intervention_type == "syrup_distribution":
            intervention_data["quantity"] = intervention.content_object.quantity
            intervention_data["units"] = "liters"
            intervention_data["syrup_type"] = intervention.content_object.syrup_type
        elif intervention.intervention_type == "harvest":
            intervention_data["quantity"] = intervention.content_object.quantity
            intervention_data["units"] = "kilos"
        elif intervention.intervention_type == "treatment":
            intervention_data["type"] = intervention.content_object.type
        elif intervention.intervention_type == "artificial_swarming":
            intervention_data["child_hive"] = intervention.content_object.__str__

        interventions.append(intervention_data)
    context = {"hive": hive.name, "interventions": interventions}
    return render(request, "interventions.html", context)
