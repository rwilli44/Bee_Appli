# Third-party imports
from django.contrib.auth.models import User
from rest_framework import serializers

# Local imports
from apiary.models import (
    BeeYard,
    Hive,
)
from .models import PublicContact


class HiveSerializerReadOnly(serializers.ModelSerializer):
    """Serializer for read-only public version of hive information.
    Unlike the private API, this one includes details on the beekeeper
    if the beekeeper has accepted sharing their information with the public."""

    beekeeper_detail = serializers.SerializerMethodField()

    class Meta:
        model = Hive
        fields = [
            "name",
            "status",
            "species",
            "date_updated",
            "beeyard_id",
            "queen_year",
            "id",
            "beekeeper_detail",
        ]

        read_only_fields = [
            "name",
            "status",
            "species",
            "date_updated",
            "beeyard_id",
            "queen_year",
            "id",
            "beekeeper_detail",
        ]

    def get_beekeeper_detail(self, obj):
        """Function to get contact details for beeekeepers which replaces
        data with 'Not Authorized' for any keepers who have not agreed to
        share their information publicly."""

        if hasattr(obj.beeyard.beekeeper, "allows_public_contact"):
            keeper = PublicContact.objects.get(
                public_beekeeper_info=obj.beeyard.beekeeper
            )
            beekeeper_detail = PublicContactSerializerReadOnly(keeper)
            return beekeeper_detail.data
        else:
            anonymous = {
                "first_name": "Not Authorized",
                "last_name": "Not Authorized",
                "email": "Not Authorized",
            }
            return anonymous


class UserSerializerReadOnly(serializers.ModelSerializer):
    """A serializer to validate beekeeper data and only allower read-only."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        read_only_fields = ["first_name", "last_name", "email"]


class PublicContactSerializerReadOnly(serializers.ModelSerializer):
    """Uses the UserSerializerReadOnly to validate contact details for
    keepers who have agreed to share their contact information."""

    public_beekeeper_info_details = UserSerializerReadOnly(
        source="public_beekeeper_info", read_only=True
    )

    class Meta:
        model = PublicContact
        fields = ["public_beekeeper_info", "public_beekeeper_info_details"]
        read_only_fields = ["public_beekeeper_info", "public_beekeeper_info_details"]


class BeeYardSerializerReadOnly(serializers.ModelSerializer):
    """Serializer that allows for read only data on beeyards and includes the details
    of the hive and the keeper while withholding information on keepers who have not
    agreed to make their information public.
    """

    hives_detailed = HiveSerializerReadOnly(source="hives", read_only=True, many=True)
    beekeeper_detail = serializers.SerializerMethodField()

    class Meta:
        model = BeeYard
        fields = ["name", "beekeeper", "hives", "hives_detailed", "beekeeper_detail"]
        read_only_fields = [
            "name",
            "beekeeper",
            "hives",
            "hives_detailed",
            "beekeeper_detail",
        ]

    def get_beekeeper_detail(self, obj):
        """Function to get contact details for beeekeepers which replaces
        data with 'Not Authorized' for any keepers who have not agreed to
        share their information publicly."""

        if hasattr(obj.beekeeper, "allows_public_contact"):
            keeper = PublicContact.objects.get(public_beekeeper_info=obj.beekeeper)
            beekeeper_detail = PublicContactSerializerReadOnly(keeper)
            return beekeeper_detail.data
        else:
            anonymous = {
                "first_name": "Not Authorized",
                "last_name": "Not Authorized",
                "email": "Not Authorized",
            }
            return anonymous
