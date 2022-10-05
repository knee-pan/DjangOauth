from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from config.permissions import IsStatisticsPermission
from machine.models import Machine


class StatisticsViewMixin:
    permission_classes = (IsAuthenticated, IsStatisticsPermission)
