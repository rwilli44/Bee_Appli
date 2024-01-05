# Third-party imports
from django.urls import path

# Local imports
from . import views


urlpatterns = [
    path("", views.show_beeyards),
    path("interventions/", views.show_interventions),
]
