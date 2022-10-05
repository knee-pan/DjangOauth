import math

from rest_framework import serializers

from machine.models import Machine, MachineType, PrintLog, Profile


class MachineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineType
        fields = ["name", "general_width", "general_height"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("updated", "created", "id")


# statistic
class MachineStatisticSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Machine
        fields = ("serial", "customer")

    def get_customer(self, obj):
        if obj.owner:
            return obj.owner.username
        return "-"


# statistic
class PrintLogStatisticSerializer(serializers.ModelSerializer):
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
    profiles = ProfileSerializer(many=True, read_only=True)
    # admin_pass_prefix_key = serializers.SerializerMethodField()

    class Meta:
        model = Machine
        fields = (
            "serial",
            "enable_stl_slc",
            "real_plate_x",
            "print_area_x",
            "print_area_y",
            "led_current",
            "z_distance",
            "heating_time",
            "heater_close_time",
            "check_status",
            "bed_heater_temp_limit",
            "autocenter",
            # "admin_pass_prefix_key",
            "profiles",
        )

    # def get_admin_pass_prefix_key(self, obj):
    #     return settings.MACHINES_ADMIN_PASS_PREFIX_KEY


class MachineLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintLog
        exclude = ("machine", "user", "ip", "software_version")


