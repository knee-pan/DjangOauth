from django.contrib import admin

#from reversion.admin import VersionAdmin
from machine.models import Machine, MachineType, Profile, Projector

# Register your models here.


admin.site.register(Profile)
admin.site.register(Projector)


@admin.register(MachineType)
class MachineTypeAdmin(admin.ModelAdmin):
    list_display = ["__str__", "general_width", "general_height"]

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin): #class MachineAdmin(VersionAdmin):
    list_display = [
        "serial",
        "mac",
        "machine_type",
        "projector_model",
        "teamviewer_id",
        "is_active",
        "owner",
        "last_activity",
        "ip",
    ]
    list_filter = [
        "is_active",
        "projector_model",
        "machine_type",
    ]
    search_fields = [
        "serial",
        "mac",]

    autocomplete_fields = ["owner"]
    ordering = ["serial"]
