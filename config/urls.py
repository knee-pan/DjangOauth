"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# from rest_framework_swagger.views import get_swagger_view

# If you haven't installed 'drf_yasg', swagger will not work.
# schema_view1 = get_swagger_view(title="Swagger UI for  API")

schema_view = get_schema_view(
    openapi.Info(
        title="Swagger UI for API",
        default_version="v1",
        description="APIs UI",
        terms_of_service="http://127.0.0.1:7000/doc/",
        contact=openapi.Contact(email="ayse"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider1")),
    path("", include("account.api.urls", namespace="acc_api")),
    path("machine/", include("machine.api.urls"), name="machine_app"),
    # url("swg", schema_view1),
    re_path(
        r"^doc(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),  # <-- Here
    path(
        "doc/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),  # <-- Here
    path(
        "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),  # <-- Here
    path("api-auth/", include("rest_framework.urls")),
    path("shop/", include("shop.api.urls", namespace="shop_api")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("api_profiler/", include("silk.urls", namespace="silk")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#  http://127.0.0.1:7000/o/applications/register/
# clientId : x6OuNUjboMa9Jq78lObiFyYNjK7C3DpCcSimfRI9
# clientSecret : BfZQUY6bwa9xTMG3ABCu8ZwBvTqdueuTaIh3QzHlqAlsh2AtTFJv00y4cDxONzz9Yrb5CcPjSOmYDWEXAbhBeS8HjdITddtgPIZdxLrd4G85nScI6JyvaKr8EYtktVB4


# Silk primarily consists of:

# Middleware for intercepting Requests/Responses
# A wrapper around SQL execution for profiling of database queries
# A context manager/decorator for profiling blocks of code and functions either manually or dynamically.
# A user interface for inspection and visualisation of the above.

# [silk] python manage.py -
# silk_clear_request_log
# silk_request_garbage_collect

# It records things like:

# Time taken
# Num. queries
# Time spent on queries
# Request/Response headers
# Request/Response bodies
# and so on.