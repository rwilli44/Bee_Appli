from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from .views import PublicAPIView

# Local imports
from public_api import views


# Create the Public API Router
class CustomRouter(routers.DefaultRouter):
    """Creates a custom view for the API so that its title shows as
    Public API"""

    def get_api_root_view(self, api_urls=None):
        return PublicAPIView.as_view()


public_router = CustomRouter()

public_router.register(r"beeyards", views.BeeYardViewSet, basename="beeyards")
public_router.register(r"hives", views.HiveViewSet, basename="hives")
public_router.register(r"beekeepers", views.BeekeeperViewSet, basename="beekeepers")

urlpatterns = []
