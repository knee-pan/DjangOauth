from django.urls import path

from machine.api.views import MachineTypeListCreateAPI

urlpatterns = [
    path("type", MachineTypeListCreateAPI.as_view(), name="list_create"),
]

# path("type", cache_page(60*60)(MachineTypeListCreateAPI.as_view()), name="list_create")
