# Third-party imports
from django.contrib.auth.models import User
from rest_framework import serializers

# Local imports
from .models import (
    BeeYard,
    Contamination,
    Hive,
    Intervention,
    Quantity,
    Treatment,
)


class ContaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contamination
        fields = ["type", "date", "hive"]


class HiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hive
        fields = ["status", "species", "date_updated", "beeyard_id", "queen_year", "id"]


class BeeYardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeeYard
        fields = ["name", "beekeeper_id"]


class ContentObjectRelatedField(serializers.RelatedField):
    """
    A serializer for the 'content object' generic relationship
    used in the Intervention model
    """

    def to_representation(self, value):
        if isinstance(value, Quantity):
            return QuantitySerializer(value).data
        elif isinstance(value, Treatment):
            return TreatmentSerializer(value).data
        elif isinstance(value, Hive):
            return HiveSerializer(value).data
        raise Exception("Unexpected type of tagged object")


class InterventionSerializer(serializers.ModelSerializer):
    content_object = ContentObjectRelatedField(read_only=True)

    class Meta:
        model = Intervention
        fields = [
            "intervention_type",
            "date",
            "hive_affected_id",
            "content_type",
            "object_id",
            "content_object",
        ]


class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity
        fields = ["quantity", "units"]


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ["treatment_type"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]
