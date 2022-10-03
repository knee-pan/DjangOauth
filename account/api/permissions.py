from pprint import pprint

from rest_framework import permissions

# SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # IsAdminUser'ın has_permission'una bak, bool döndür
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


pprint(dir(IsAdminOrReadOnly)) # has_obj , has_obj_perm
# has_obj: her daim, has_obj_perm: tetiklendiğinde çalışır


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
