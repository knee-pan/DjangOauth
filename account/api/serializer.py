from rest_framework import routers, serializers, viewsets

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "is_staff", "first_name", "last_name"]
