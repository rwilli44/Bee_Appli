# Third-party imports
from django.urls import path
from django.contrib.auth.models import AnonymousUser
from rest_framework import routers

# Local imports
from . import views


urlpatterns = [
    # Show connected user's hive details
    path("", views.show_beeyards, name="show_beeyards"),
    # Show connected user's hives' interventions
    path("interventions/", views.show_interventions),
]


# Create a custom router to set the default list view to only show
# beeyards/hives/interventions that belong to the authenticated beekeeper
class CustomRouter(routers.DefaultRouter):
    routes = [
        # Define a custom route for the list action
        routers.Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "filtered_list", "post": "create"},
            name="{basename}-filtered-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        routers.Route(
            url=r"^{prefix}/{lookup}{trailing_slash}$",
            mapping={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Detail"},
        ),
    ]


# Register the viewsets with the custom router
router = CustomRouter()
router.register(r"beeyards", views.BeeYardViewSet, basename="beeyards")
router.register(r"hives", views.HiveViewSet, basename="hives")
router.register(r"interventions", views.InterventionViewSet, basename="interventions")
