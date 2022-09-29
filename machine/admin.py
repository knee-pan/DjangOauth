from django.contrib import admin

from machine.models import MachineType, Profile

# Register your models here.

admin.site.register(MachineType)
admin.site.register(Profile)
