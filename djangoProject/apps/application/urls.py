from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.application.views import DriverApplicationViewSet

application_router = DefaultRouter()
application_router.register(prefix='', viewset=DriverApplicationViewSet, basename='applications')


urlpatterns = [
    path('', include(application_router.urls)),
]