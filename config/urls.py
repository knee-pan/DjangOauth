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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider1")),
    path("", include("account.api.urls", namespace="acc_api")),
    path("machine/", include("machine.api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#  http://127.0.0.1:7000/o/applications/register/
# clientId : x6OuNUjboMa9Jq78lObiFyYNjK7C3DpCcSimfRI9
# clientSecret : BfZQUY6bwa9xTMG3ABCu8ZwBvTqdueuTaIh3QzHlqAlsh2AtTFJv00y4cDxONzz9Yrb5CcPjSOmYDWEXAbhBeS8HjdITddtgPIZdxLrd4G85nScI6JyvaKr8EYtktVB4
