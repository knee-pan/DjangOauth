from django.urls import path

from shop.api.views import (
    CategoryCreateAPI,
    CategoryDestroyAPI,
    CategoryListAPI,
    CategoryUpdateAPI,
)

app_name = "shop_api"
urlpatterns = [
    path("category/list/", CategoryListAPI.as_view(), name="list"),
    path("category/create", CategoryCreateAPI.as_view(), name="create"),
    path("category/update/<pk>", CategoryUpdateAPI.as_view(), name="update"),
    path("category/delete/<pk>", CategoryDestroyAPI.as_view(), name="destroy"),
]
