from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from logs.views import LogViewSet

router = DefaultRouter()
router.register(r'logs', LogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logs/', include('logs.urls')),
    path('api/', include(router.urls)),
]