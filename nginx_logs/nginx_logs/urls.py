from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include

schema_view = get_schema_view(
    openapi.Info(
        title="Nginx Logs API",
        default_version="v1",
        description="API for Nginx Logs",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("logs.urls")),
    # Swagger UI
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # Raw schema in JSON format
    path("swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    # Raw schema in YAML format
    path("swagger.yaml/", schema_view.without_ui(cache_timeout=0), name="schema-yaml"),
]
