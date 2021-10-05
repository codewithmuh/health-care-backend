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
        response = []
        respiratory = self.request.user.user_measurements.filter(category="respiratory").first()
        oxygen = self.request.user.user_measurements.filter(category="oxygen").first()
        heart_rate = self.request.user.user_measurements.filter(category="heart_rate").first()
        viscosity = self.request.user.user_measurements.filter(category="viscosity").first()
        temperature = self.request.user.user_measurements.filter(category="temperature").first()
        if respiratory:
            response.append({"title": "respiratory", "value": respiratory.value})
        if oxygen:
            response.append({"title": "oxygen", "value": oxygen.value})
        if heart_rate:
            response.append({"title": "heart_rate", "value": heart_rate.value})
        if viscosity:
            response.append({"title": "viscosity", "value": viscosity.value})
        if temperature:
            response.append({"title": "temperature", "value": temperature.value})
        return Response(response)
