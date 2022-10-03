from django.urls import path

from machine.api.views import MachineTypeListCreateAPI, ProfileListAPI, ProfileCreateAPI

urlpatterns = [
    path("type", MachineTypeListCreateAPI.as_view(), name="list_create"),
    path("profiles", ProfileListAPI.as_view(), name="profiles"),
    path("profile_create", ProfileCreateAPI.as_view(), name="profile_create"),
]

# path("type", cache_page(60*60)(MachineTypeListCreateAPI.as_view()), name="list_create")
