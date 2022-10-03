from ..models import User
from rest_framework import routers, serializers, viewsets


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','is_staff','first_name','last_name']
