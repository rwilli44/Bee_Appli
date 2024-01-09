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
    class Meta:
        model = Hive
        fields = [
            "status",
            "species",
            "date_updated",
            "beeyard_id",
            "queen_year",
            "id",
        ]

        read_only_fields = [
            "status",
            "species",
            "date_updated",
            "beeyard_id",
            "queen_year",
            "id",
        ]


class BeeYardSerializerReadOnly(serializers.ModelSerializer):
    hives_detailed = HiveSerializerReadOnly(source="hives", read_only=True, many=True)

    class Meta:
        model = BeeYard
        fields = ["name", "beekeeper_id", "hives", "hives_detailed"]
        read_only_fields = ["name", "beekeeper_id", "hives", "hives_detailed"]


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
