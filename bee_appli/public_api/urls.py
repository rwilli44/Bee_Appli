# Third-party imports
from rest_framework import routers

# Local imports
from public_api import views


# The title of this class will serve as the API title and the docstring will
# appear as the description replacing API Root and Default info.
class BeeAppliPublicAPI(routers.APIRootView):
    """
    Public access to details on beeyards and hives. Contact information
    available for beekeepers who have accepted to share it.
    """

    pass


class DocumentedPublicRouter(routers.DefaultRouter):
    APIRootView = BeeAppliPublicAPI


# Router for the public API
public_router = DocumentedPublicRouter()

public_router.register(r"beeyards", views.BeeYardViewSet, basename="beeyards")
public_router.register(r"hives", views.HiveViewSet, basename="hives")
public_router.register(r"beekeepers", views.BeekeeperViewSet, basename="beekeepers")

urlpatterns = []
