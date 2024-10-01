from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import NginxLogViewSet

router = DefaultRouter()
router.register(r'logs', NginxLogViewSet, basename='nginxlog')

urlpatterns = [
    path('api/', include(router.urls)),
]
