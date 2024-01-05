from django.shortcuts import render
from django.template import loader
from rest_framework import permissions, status, viewsets
from django.http import HttpResponse, JsonResponse

from .models import BeeYard, Hive, Intervention
from .serializers import BeeYardSerializer, HiveSerializer, InterventionSerializer


##### Template Views #####
def show_beeyards(request):
    """Returns a view of all the bee yards and hives of the connected user."""
    beeyard_query = BeeYard.objects.filter(beekeeper=request.user).values()
    if len(beeyard_query) == 0:
        print("check")
        return render(request, "index.html", {"beeyard_data": None})
    data = []
    for beeyard in beeyard_query:
        hive_queery = Hive.objects.filter(beeyard=beeyard["id"]).values()
        beeyard_data = BeeYardSerializer(beeyard).data
        hive_data = HiveSerializer(hive_queery, many=True).data
        data.append({"beeyard_name": beeyard_data["name"], "hives": hive_data})

    # create the json type object to pass the query results to the template
    context = {"beeyard_data": data, "user": request.user.username}
    # return an http response to the request with the filled-in template
    return render(request, "index.html", context)


def show_interventions(request):
    hive_id = request.GET["hive"]
    hive_query = Hive.objects.filter(id=hive_id).values()

    if len(hive_query) == 0:
        return render(
            request,
            "404.html",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    beeyard_id = hive_query[0]["beeyard_id"]
    beeyard = BeeYard.objects.filter(id=beeyard_id).values()
    if beeyard[0]["beekeeper_id"] != request.user.id:
        return render(
            request,
            "404.html",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    intervention_queery = Intervention.objects.filter(hive_affected=hive_id).values()

    interventions = InterventionSerializer(intervention_queery, many=True).data
    context = {"interventions": interventions, "hive": hive_id}
    return render(request, "interventions.html", context)
