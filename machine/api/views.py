from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import SAFE_METHODS, BasePermission

from config import settings

from ..models import MachineType, Profile
from .permissions import IsAdminOrReadOnly
from .serializer import MachineTypeSerializer, ProfileSerializer

# from rest_framework.response import Response


# redis-cli monitor :If you have configured everything corretly the terminal should output "GET" and "SET" requests when visiting pages that are included in the ModelViewSet along the following lines..
# @method_decorator(vary_on_cookie)
# @method_decorator(cache_page(settings.CACHE_TTL))


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


@method_decorator([vary_on_cookie, cache_page(settings.CACHE_TTL)], name="dispatch")
class MachineTypeListCreateAPI(ListCreateAPIView):
    serializer_class = MachineTypeSerializer
    queryset = MachineType.objects.all()
    # permission_classes = [IsAuthenticated | ReadOnly]

    # def get(self, request, format=None):
    #     content = {"status": "request was permitted"}
    #     return Response(content)


class ProfileListAPI(ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 60))
    def dispatch(self, *args, **kwargs):
        return super(ProfileListAPI, self).dispatch(*args, **kwargs)


class ProfileCreateAPI(CreateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    # def get_queryset(self):
    #     return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return super().perform_create(serializer)
