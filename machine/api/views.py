from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    get_object_or_404,
)

from ...config import settings
from ..models import MachineType, Profile
from .serializer import MachineTypeSerializer, ProfileSerializer

# redis-cli monitor :If you have configured everything corretly the terminal should output "GET" and "SET" requests when visiting pages that are included in the ModelViewSet along the following lines..


@method_decorator(vary_on_cookie)
@method_decorator(cache_page(settings.CACHE_TTL))
class MachineTypeListCreateAPI(ListCreateAPIView):
    serializer_class = MachineTypeSerializer
    queryset = MachineType.objects.all()


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

    def perform_create(self, serializer):
        return super().perform_create(serializer)
