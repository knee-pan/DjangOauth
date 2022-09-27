# DjangOauth
Django Oauth Sample

* python manage.py createsuperuser
* django-admin startapp account
* pipenv install django-oauth-toolkit

INSTALLED_APPS = [
    ...
    "oauth2_provider",
]


urlpatterns = [
    ...
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]