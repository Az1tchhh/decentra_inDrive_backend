from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from apps.application.models import DriverApplication
from apps.application.serializers import DriverApplicationSerializer, DriverApplicationCreateSerializer
from apps.application.services import add_driver_application, model_validation
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
        'update_status': None
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

    @action(methods=['GET'], url_path='validate', detail=True)
    def validate(self, request, *args, **kwargs):
        obj = self.get_object()
        updated_object = model_validation(obj)
        serializer = self.get_serializer(updated_object)
        return Response(serializer.data)

    @action(methods=['POST'], url_path='update-status', detail=True)
    def update_status(self, request, *args, **kwargs):
        status_ = self.request.query_params.get('status')
        obj = self.get_object()
        obj.status = status_
        obj.save(update_fields=['status'])
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
