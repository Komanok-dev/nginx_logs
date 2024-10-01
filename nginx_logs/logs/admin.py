from django.contrib import admin
from .models import NginxLog


@admin.register(NginxLog)
class NginxLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "log_time", "http_method", "uri", "response_code")
    list_filter = ("http_method", "response_code", "log_time")
    search_fields = ("ip_address", "uri", "user_agent")
