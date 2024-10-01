from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from .models import NginxLog
from .serializers import NginxLogSerializer


class NginxLogViewSet(viewsets.ModelViewSet):
    queryset = NginxLog.objects.all().order_by("log_time")
    serializer_class = NginxLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["http_method", "response_code"]
    search_fields = ["ip_address", "uri", "user_agent"]
