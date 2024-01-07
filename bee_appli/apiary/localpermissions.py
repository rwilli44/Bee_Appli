# Third-party imports
from rest_framework.permissions import BasePermission, SAFE_METHODS

# Local imports
from .models import BeeYard


class IsKeeperOrReadOnly(BasePermission):
    """Used to ensure only an animal's keeper can edit its data."""

    def has_object_permission(self, request, view, obj):
        # allow read-only
        if request.method in SAFE_METHODS:
            return True

        if obj.beekeeper == request.user:
            return True
        return False
