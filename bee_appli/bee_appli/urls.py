from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

# Local imports
from apiary import views
from .settings import DEBUG


# Create a custom router to set the default list view to only show
# beeyards/hives/interventions that belong to the authenticated beekeeper
class CustomRouter(routers.DefaultRouter):
    routes = [
        # Define a custom route for the list action
        routers.Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "filtered_list"},
            name="{basename}-filtered-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
    ]


# Register the viewsets with the custom router
router = CustomRouter()
router.register(r"beeyards", views.BeeYardViewSet, basename="beeyards")
router.register(r"hives", views.HiveViewSet, basename="hives")
router.register(r"interventions", views.InterventionViewSet, basename="interventions")


urlpatterns = [
    # Custom router for beekeper API
    path("", include(router.urls)),
    # Honeypot fake admin login
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    # Actual admin login
    path("apiaryadminaccessportal/", admin.site.urls),
    # URLs for template-based views
    path("apiary/", include("apiary.urls")),
]

# Needed to show the sidebar in admin when in debug mode
if DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(r"__debug__/", include(debug_toolbar.urls)),
    ]
