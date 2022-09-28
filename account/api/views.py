from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView


# 403
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, OAuth2!")


@login_required()
def dashboard(request, *args, **kwargs):
    return HttpResponse("Login required", status=200)
