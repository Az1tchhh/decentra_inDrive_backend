from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from apps.application.models import DriverApplication
from apps.application.serializers import DriverApplicationSerializer, DriverApplicationCreateSerializer
from apps.application.services import add_driver_application
from apps.utils.views import BaseViewSet
from config.parsers import DrfNestedParser


# Create your views here.
class DriverApplicationViewSet(BaseViewSet,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):
    queryset = DriverApplication.objects.order_by('-created_at')
    serializer_class = DriverApplicationSerializer
    parser_classes = (DrfNestedParser, JSONParser)
    serializers = {
        'create': DriverApplicationCreateSerializer,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def perform_create(self, serializer):
        application = add_driver_application(serializer.validated_data)
        return application

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)
        serializer = DriverApplicationSerializer(data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
