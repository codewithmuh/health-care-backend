from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import MeasurementViewSets, HistoryAPIView

router = DefaultRouter()
router.register('measurement', MeasurementViewSets , basename='measurement')

urlpatterns = [
    path("", include(router.urls)),
    path("history/", HistoryAPIView.as_view(), name='history')
]
