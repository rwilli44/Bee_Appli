# Third-party imports
from django.urls import path
from django.contrib.auth.models import AnonymousUser

# Local imports
from . import views


urlpatterns = [
    # Show connected user's hive details
    path("", views.show_beeyards, name="show_beeyards"),
    # Show connected user's hives' interventions
    path("interventions/", views.show_interventions),
]
