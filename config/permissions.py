from rest_framework import permissions


class IsProviderPermission(permissions.BasePermission):
    """
    Global permission check for Providers.
    """

    def has_permission(self, request, view):
        return request.user.applications.filter(name="PcSlicer").exists()


class CanCreateNovaPermission(permissions.BasePermission):
    """
    Global permission check for Create Nova.
    """

    def has_permission(self, request, view):
        return request.user.company.can_create_nova


class IsOperatorPermission(permissions.BasePermission):
    """
    Global permission check for Operators.
    """

    def has_permission(self, request, view):
        return request.user.applications.filter(name="MegaPlatform").exists()


class IsViewerPermission(permissions.BasePermission):
    """
    Global permission check for Viewers.
    """

    def has_permission(self, request, view):
        return request.user.applications.filter(name="Frontend").exists()


class IsStatisticsPermission(permissions.BasePermission):
    """
    Global permission check for Statistics.
    """

    def has_permission(self, request, view):
        return request.user.applications.filter(name="Statistics").exists()
