from django.db.models import Count, F, FloatField, Sum, Value
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission

from config import settings
from config.mixins import StatisticsViewMixin

from ..models import Machine, MachineType, PrintLog, Profile
from .permissions import IsAdminOrReadOnly
from .serializer import (
    MachineLogSerializer,
    MachineSerializer,
    MachineTypeSerializer,
    ProfileSerializer,
)

# redis-cli monitor :If you have configured everything corretly the terminal should output "GET" and "SET" requests when visiting pages that are included in the ModelViewSet along the following lines..
# @method_decorator(vary_on_cookie)
# @method_decorator(cache_page(settings.CACHE_TTL))


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


@method_decorator([vary_on_cookie, cache_page(cache_page(60 * 60))], name="dispatch")
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

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


# class ProfileCreateAPI -> acc appinde de mevcut ismi değiş


class MachineDetail(RetrieveAPIView):
    serializer_class = MachineSerializer
    queryset = Machine.objects.all()
    lookup_field = "pk"


class MachineListCreateAPI(ListCreateAPIView):
    serializer_class = MachineSerializer
    queryset = Machine.objects.all()


class LogListCreateAPI(ListCreateAPIView):
    serializer_class = MachineLogSerializer
    queryset = PrintLog.objects.all()


# Verileri Cache hazırla.
# urle ekle.
class DashboardAPI(RetrieveAPIView, StatisticsViewMixin):
    @method_decorator(cache_page(60 * 60))
    def get(self, request, *args, **kwargs):
        machine_ips = (
            Machine.objects.exclude(ip=None).values("ip").annotate(total=Count("ip"))
        )
        total_machine = Machine.objects.count()
        total_print = PrintLog.objects.count()

        # last 24 hour active machine
        date_from = timezone.now() - timezone.timedelta(days=1)
        # gt (greater than, or equal to)
        last_24h_total_active_machine = Machine.objects.filter(
            last_activity__gte=date_from
        ).count()
        # last 24 hour print
        last_24h_print = PrintLog.objects.filter(created__gte=date_from)

        last_24h_total_print = last_24h_print.count()
        last_24h_total_faulty_print = last_24h_print.filter(
            print_status="faulty"
        ).count()
        last_24h_total_cancelled_print = last_24h_print.filter(
            print_status="cancelled"
        ).count()
        last_24h_total_unsuccessful_print = last_24h_print.filter(
            print_status="unsuccessful"
        ).count()
        last_24h_total_successful_print = last_24h_print.filter(
            print_status="successful"
        ).count()

        # last week active objects

        date_from_week = timezone.now() - timezone.timedelta(days=7)

        # recine hesabi
        total_resin = (
            PrintLog.objects.filter(
                print_stop__gte=date_from_week, total_solid_area__range=(0, 50)
            )
            .aggregate(
                total_spent=Sum(
                    F("total_solid_area") * Value(0.0023), output_field=FloatField()
                )
            )
            .get("total_spent")
        )

        if total_resin is None:
            total_resin = 0.0

        content = {
            "total_machine": total_machine,
            "last_24h_total_active_machine": last_24h_total_active_machine,
            # 'total_client': total_client,
            "total_print": total_print,
            "last_24h_total_print": last_24h_total_print,
            "last_24h_total_successful_print": last_24h_total_successful_print,
            "last_24h_total_unsuccessful_print": last_24h_total_unsuccessful_print,
            "last_24h_total_cancelled_print": last_24h_total_cancelled_print,
            "last_24h_total_faulty_print": last_24h_total_faulty_print,
            "total_resin": "%.1f" % total_resin,
            "machine_ips": [entry for entry in machine_ips],
        }
        return JsonResponse(content)
