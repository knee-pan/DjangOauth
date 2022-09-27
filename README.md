# DjangOauth
Django Oauth Sample

* python manage.py createsuperuser
* django-admin startapp account
* pipenv install django-oauth-toolkit

INSTALLED_APPS = [
    ...
    "account",
    "oauth2_provider",
]


urlpatterns = [
    ...
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

* Yeni bir projeye başlıyorsanız, varsayılan Users modeli sizin için yeterli olsa bile özel bir Users modeli kurmanız önemle tavsiye edilir.
* Bu model, varsayılan user modeliyle aynı şekilde davranır, ancak ihtiyaç duyulursa gelecekte bunu özelleştirebileceksiniz. 

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

* settings.py'da hangi user modelinin kullanılacağını belirtmek gerek : AUTH_USER_MODEL='account.User'

* python manage.py makemigrations, migrate

* This will make available endpoints to authorize, generate token and create OAuth applications.

* Last change, add LOGIN_URL to iam/settings.py: LOGIN_URL='/admin/login/'





