from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from .serializers import MeasurementSerializer
from backapi.models import Measurement
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class StandardResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page'
    max_page_size = 100


class MeasurementViewSets(ModelViewSet):
    queryset = Measurement.objects.none()
    serializer_class = MeasurementSerializer
    filterset_fields = ['category']

    def get_queryset(self):
        queryset = Measurement.objects.filter(user=self.request.user)
        return queryset

