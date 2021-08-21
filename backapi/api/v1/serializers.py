from rest_framework import serializers
from backapi.models import Measurement, DeductCreditSetting


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = ['user', 'category', 'value']
        
    def validate(self, attrs):
        cleaned_data = super(MeasurementSerializer, self).validate(attrs)
        user = cleaned_data.get('user')
        credit_to_deduct = 1
        threshold = DeductCreditSetting.objects.first()
        if threshold:
            credit_to_deduct = threshold.amount
        if user.credits <= credit_to_deduct:
            raise serializers.ValidationError({"user": f"Must have {credit_to_deduct} credits, please purchase first."})
