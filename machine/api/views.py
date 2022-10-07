from django.core.cache import cache
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
from silk.profiling.profiler import silk_profile

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


# @method_decorator([vary_on_cookie, cache_page(cache_page(60 * 60))], name="dispatch")
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
    # @method_decorator(cache_page(60 * 60)) # cache_page(saniye * adet)
    @silk_profile(name="View Dashboard")
    def get(self, request, *args, **kwargs):
        machine_ips = (
            Machine.objects.exclude(ip=None).values("ip").annotate(total=Count("ip"))
        )
        total_machine = Machine.objects.count()
        total_print = PrintLog.objects.count()

        cache.set('machine_count_cache', Machine.objects.count())
        cache.set('log_count_cache', PrintLog.objects.count())

        # last 24 hour active machine
        date_from = timezone.now() - timezone.timedelta(days=1)
        # gt (greater than, or equal to)
        last_24h_total_active_machine = Machine.objects.filter(
            last_activity__gte=date_from
        ).count()
        # last 24 hour print
        # last_24h_print = PrintLog.objects.filter(created__gte=date_from)

        # last_24h_total_print = last_24h_print.count()
        # last_24h_total_faulty_print = last_24h_print.filter(
        #     print_status="faulty"
        # ).count()
        # last_24h_total_cancelled_print = last_24h_print.filter(
        #     print_status="cancelled"
        # ).count()
        # last_24h_total_unsuccessful_print = last_24h_print.filter(
        #     print_status="unsuccessful"
        # ).count()
        # last_24h_total_successful_print = last_24h_print.filter(
        #     print_status="successful"
        # ).count()

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

        # Eğer reçine hesabını 30 saniyede bir gibi bir sürede cachelemek istiyorsak:
        cache.set('total_resin_cache',str(
            PrintLog.objects.filter(
                print_stop__gte=date_from_week, total_solid_area__range=(0, 50)
            )
            .aggregate(
                total_spent=Sum(
                    F("total_solid_area") * Value(0.0023), output_field=FloatField()
                )
            )
            .get("total_spent")
        ), 30)

        print(
            [log for log in PrintLog.objects.filter(created__gte=date_from).values("print_status").annotate(count=Count("print_status"))]
        )
        content = {
            "total_machine": total_machine,
            "machine_count_cache": cache.get('machine_count_cache'),
            "last_24h_total_active_machine": last_24h_total_active_machine,
            # 'total_client': total_client,
            "total_print": total_print,
            "log_count_cache": cache.get('log_count_cache'),
            "Printlog":[log for log in PrintLog.objects.filter(created__gte=date_from).values("print_status").annotate(count=Count("print_status"))],
            "total_resin": "%.1f" % total_resin,
            "total_resin_cache": cache.get('total_resin_cache'),
            "machine_ips": [entry for entry in machine_ips],
            "Machine Count":cache.get_or_set('count', Machine.objects.count(), 100)
        }
        return JsonResponse(content)
