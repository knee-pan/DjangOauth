import math

from rest_framework import serializers

from machine.models import MachineType, PrintLog, Profile, Machine


class MachineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineType
        fields = ["name", "general_width", "general_height"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("updated", "created", "id")


class PrintLogSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    print_time = serializers.SerializerMethodField()
    machine = serializers.SerializerMethodField()
    print_status = serializers.SerializerMethodField()

    class Meta:
        model = PrintLog
        fields = (
            "id",
            "customer",
            "print_time",
            "machine",
            "print_status",
        )

    def get_customer(self, obj):
        return obj.user.company.name

    def get_print_time(self, obj):
        return f"{math.floor((obj.print_stop - obj.print_start).seconds / 60)} min"

    def get_machine(self, obj):
        return obj.machine.serial[-4:-1]

    def get_print_status(self, obj):
        return obj.get_print_status_display()


class MachineSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Machine
        fields = ("serial", "customer")

    def get_customer(self, obj):
        if obj.owner:
            return obj.owner.username
        return "-"