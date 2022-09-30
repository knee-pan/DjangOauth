from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from models import User
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework.generics import CreateAPIView
from serializer import UserSerializer
from throttles import RegisterThrottle


# 403
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, OAuth2!")


@login_required()
def dashboard(request, *args, **kwargs):
    return HttpResponse("Login required", status=200)


class UserCreate(CreateAPIView):
    serializer_class = UserSerializer
    throttle_classes = [RegisterThrottle]
    queryset = User.objects.all()
