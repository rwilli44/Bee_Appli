# Third-party imports
from django.contrib.auth.models import User
from rest_framework import serializers

# Local imports
from .models import (
    BeeYard,
    Contamination,
    Hive,
    Intervention,
    Harvest,
    SyrupDistribution,
    Treatment,
)


class ContaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contamination
        fields = ["type", "date", "hive"]


class HiveSerializer(serializers.ModelSerializer):
    interventions = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="intervention"
    )
    contaminations = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="contaminations"
    )

    class Meta:
        model = Hive
        fields = [
            "status",
            "species",
            "date_updated",
            "beeyard_id",
            "queen_year",
            "id",
            "interventions",
            "contaminations",
        ]


class BeeYardSerializer(serializers.ModelSerializer):
    hives_detailed = HiveSerializer(source="hives", read_only=True, many=True)
    hives = serializers.SlugRelatedField(many=True, read_only=True, slug_field="hive")

    class Meta:
        model = BeeYard
        fields = ["name", "beekeeper_id", "hives", "hives_detailed"]


class ContentObjectRelatedField(serializers.RelatedField):
    """
    A serializer for the 'content object' generic relationship
    used in the Intervention model
    """

    def to_representation(self, value):
        if isinstance(value, Harvest):
            return HarvestSerializer(value).data
        elif isinstance(value, SyrupDistribution):
            return SyrupDistributionSerializer(value).data
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


class HarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = ["quantity"]


class SyrupDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyrupDistribution
        fields = ["quantity", "syrup_type"]


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ["treatment_type"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    beeyards = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="beeyard"
    )

    class Meta:
        model = User
        fields = ["url", "username", "email", "groups", "beeyards"]
