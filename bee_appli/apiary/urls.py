# Third-party imports
from django.contrib.auth.models import AnonymousUser
from django.urls import path
from rest_framework import routers

# Local imports
from . import views

# Create a router to organize API views
router = routers.DefaultRouter()

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
