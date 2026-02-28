# DRF
from rest_framework import serializers

from learning.models import LearningResource, LearningUnit


class LearningResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResource
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class LearningUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningUnit
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
