from rest_framework import filters, permissions
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
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
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['category']

    def get_queryset(self):
        queryset = Measurement.objects.filter(user=self.request.user)
        return queryset


class HistoryAPIView(APIView):
    queryset = Measurement.objects.none
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = {}
        respiratory = self.request.user.user_measurements.filter(category="respiratory").first()
        oxygen = self.request.user.user_measurements.filter(category="oxygen").first()
        heart_rate = self.request.user.user_measurements.filter(category="heart_rate").first()
        viscosity = self.request.user.user_measurements.filter(category="viscosity").first()
        temperature = self.request.user.user_measurements.filter(category="temperature").first()
        if respiratory:
            response.update({"respiratory": respiratory.value})
        if oxygen:
            response.update({"oxygen": oxygen.value})
        if heart_rate:
            response.update({"heart_rate": heart_rate.value})
        if viscosity:
            response.update({"viscosity": viscosity.value})
        if temperature:
            response.update({"temperature": temperature.value})
        return Response(response)

