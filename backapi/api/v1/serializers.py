from rest_framework import serializers
from backapi.models import Measurement


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = ['user', 'category', 'value']
