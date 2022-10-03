from pprint import pprint

from rest_framework import permissions

# SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # IsAdminUser'ın has_permission'una bak, bool döndür
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin
