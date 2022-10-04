from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAdminUser

# from ..models import User
from .permissions import IsAdminOrReadOnly
from .serializer import UserCreateSerializer, UserSerializer
from .throttles import RegisterThrottle


# 403
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, OAuth2!")


@login_required()
def dashboard(request, *args, **kwargs):
    return HttpResponse("Login required", status=200)


class ProfileUpdateAPI(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # lookup_field = "pk"  # default pk

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class UserList(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [
        RegisterThrottle,
    ]


class UserCreate(CreateAPIView):  # register
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    throttle_classes = [
        RegisterThrottle,
    ]
