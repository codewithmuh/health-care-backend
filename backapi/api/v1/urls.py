from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import MeasurementViewSets

router = DefaultRouter()
router.register('measurement', MeasurementViewSets , basename='measurement')

urlpatterns = [
    path("", include(router.urls)),
]
