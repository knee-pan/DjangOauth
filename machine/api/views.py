from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    get_object_or_404,
)
from ...config import settings
from ..models import MachineType, Profile
from .serializer import MachineTypeSerializer, ProfileSerializer

CACHE_TTL=getattr(settings,'CACHE_TTL',DEFAULT_TIMEOUT)

class MachineTypeListCreateAPI(ListCreateAPIView):
    serializer_class = MachineTypeSerializer
    queryset = MachineType.objects.all()


class ProfileListAPI(ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class ProfileCreateAPI(CreateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def perform_create(self, serializer):
        return super().perform_create(serializer)
