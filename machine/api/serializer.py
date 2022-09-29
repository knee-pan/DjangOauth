from rest_framework import serializers

from machine.models import MachineType, Profile


class MachineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineType
        fields = ["name", "general_width", "general_height"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("updated", "created", "id")
