# Third-party imports
from rest_framework.permissions import BasePermission, SAFE_METHODS

# Local imports
from .models import BeeYard, Hive, Intervention


class IsKeeperOrReadOnly(BasePermission):
    """Used to ensure only a beeyard's beekeeper can edit its data,
    but anyone can read it."""

    def has_object_permission(self, request, view, obj):
        # allow read-only
        if request.method in SAFE_METHODS:
            return True

        if obj.beekeeper == request.user:
            return True
        return False


class IsKeeper(BasePermission):
    """Used to ensure only a beeyard's beekeeper can edit its data."""

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, BeeYard):
            return obj.beekeeper == request.user
        elif isinstance(obj, Intervention):
            hive = Hive.objects.get(id=obj.hive_affected_id)
            return hive.beeyard.beekeeper == request.user
        elif isinstance(obj, Hive):
            return obj.beeyard.beekeeper == request.user
        return False
