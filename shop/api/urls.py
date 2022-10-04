from django.urls import path

from shop.api.views import (
    CategoryCreateAPI,
    CategoryDestroyAPI,
    CategoryListAPI,
    CategoryUpdateAPI,
    ProductListAPI,
    ProductCreateAPI,
    ProductUpdateAPI,
    ProductDestroyAPI,
    ProductDetailAPI
)

app_name = "shop_api"
urlpatterns = [
    path("category/list/", CategoryListAPI.as_view(), name="list"),
    path("category/create", CategoryCreateAPI.as_view(), name="create"),
    path("category/update/<pk>", CategoryUpdateAPI.as_view(), name="update"),
    path("category/delete/<pk>", CategoryDestroyAPI.as_view(), name="destroy"),

    path("prod/list/", ProductListAPI.as_view(), name="list"),
    path("prod/create", ProductCreateAPI.as_view(), name="create"),
    path("prod/detail/<pk>", ProductDetailAPI.as_view(), name="detail"),
    path("prod/update/<pk>", ProductUpdateAPI.as_view(), name="update"),
    path("prod/delete/<pk>", ProductDestroyAPI.as_view(), name="destroy"),
]
