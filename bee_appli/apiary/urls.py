# Third-party imports
from django.contrib.auth.models import AnonymousUser
from django.urls import path
from rest_framework import routers

# Local imports
from . import views


# The title of this class will serve as the API title and the docstring will
# appear as the description replacing API Root and Default info.
class BeeAppliPrivateApiaryAPI(routers.APIRootView):
    """
    Private API for access to details on beeyards, hives, interventions and
    contaminations. Information is only available to authenticated users and
    only allows access to their one beeyard/hive information.
    """

    pass


class DocumentedPrivateRouter(routers.DefaultRouter):
    APIRootView = BeeAppliPrivateApiaryAPI


# Create a router to organize API views
router = DocumentedPrivateRouter()

# Register API views to the router
router.register(r"beeyards", views.BeeYardViewSet, basename="beeyards")
router.register(r"hives", views.HiveViewSet, basename="hives")
router.register(r"interventions", views.InterventionViewSet, basename="interventions")
router.register(
    r"contaminations", views.ContaminationViewSet, basename="contaminations"
)


urlpatterns = [
    # Show connected user's hive details
    path("", views.show_beeyards, name="show_beeyards"),
    # Show connected user's hives' interventions
    path("interventions/", views.show_interventions),
    # Beekeeper login
    path("login", views.LoginInterfaceView.as_view(), name="login"),
    # Beekeeper logout
    path("logout", views.logout_request, name="logout"),
]
