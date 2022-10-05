from django.contrib import admin

from machine.models import MachineType, Profile, Projector

# Register your models here.


admin.site.register(Profile)
admin.site.register(Projector)


@admin.register(MachineType)
class MachineTypeAdmin(admin.ModelAdmin):
    list_display = ["__str__", "general_width", "general_height"]
