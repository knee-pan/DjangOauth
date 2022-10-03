from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework.generics import CreateAPIView, ListAPIView

from ..models import User
from .permissions import IsAdminOrReadOnly
from .serializer import UserSerializer
from .throttles import RegisterThrottle


# 403
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, OAuth2!")


@login_required()
def dashboard(request, *args, **kwargs):
    return HttpResponse("Login required", status=200)


class UserList(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [
        RegisterThrottle,
    ]


class UserCreate(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [
        RegisterThrottle,
    ]
