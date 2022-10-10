from django.urls import path

from machine.api.views import (
    DashboardAPI,
    LogListCreateAPI,
    MachineDetail,
    MachineListAPI,
    MachineCreateAPI,
    MachineTypeListCreateAPI,
    ProfileCreateAPI,
    ProfileListAPI,
)

app_name = "machine_app"
urlpatterns = [
    path("type/", MachineTypeListCreateAPI.as_view(), name="type_list_create"),
    path("profiles/", ProfileListAPI.as_view(), name="profiles"),
    path("profile_create/", ProfileCreateAPI.as_view(), name="profile_create"),
    path("detail/<pk>", MachineDetail.as_view(), name="detail"),
    path("list/", MachineListAPI.as_view(), name="list"),
    path("create/", MachineCreateAPI.as_view(), name="create"),
    path("log_list/", LogListCreateAPI.as_view(), name="log_list"),
    path("dashboard_cache/", DashboardAPI.as_view(), name="dashboard_cache"),
]

# path("dashboard_cache/", cache_page(60*60)(DashboardAPI.as_view()), name="dashboard_cache")
