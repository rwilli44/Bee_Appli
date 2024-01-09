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
        if hasattr(obj.beeyard.beekeeper, "allows_public_contact"):
            keeper = PublicContact.objects.get(
                public_beekeeper_info=obj.beeyard.beekeeper
            )
            beekeeper_detail = PublicContactSerializer(keeper)
            return beekeeper_detail.data
        else:
            anonymous = {
                "first_name": "Not Authorized",
                "last_name": "Not Authorized",
                "email": "Not Authorized",
            }
            return anonymous


class UserSerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        read_only_fields = ["first_name", "last_name", "email"]


class PublicContactSerializer(serializers.ModelSerializer):
    public_beekeeper_info_details = UserSerializerReadOnly(
        source="public_beekeeper_info", read_only=True
    )

    class Meta:
        model = PublicContact
        fields = ["public_beekeeper_info", "public_beekeeper_info_details"]
        read_only_fields = ["public_beekeeper_info", "public_beekeeper_info_details"]


class BeeYardSerializerReadOnly(serializers.ModelSerializer):
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
        if hasattr(obj.beekeeper, "allows_public_contact"):
            keeper = PublicContact.objects.get(public_beekeeper_info=obj.beekeeper)
            beekeeper_detail = PublicContactSerializer(keeper)
            return beekeeper_detail.data
        else:
            anonymous = {
                "first_name": "Not Authorized",
                "last_name": "Not Authorized",
                "email": "Not Authorized",
            }
            return anonymous
