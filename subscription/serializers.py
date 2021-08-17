from rest_framework import serializers
from .models import CreditsSetting

class CardDetailSerializer(serializers.Serializer):
    card_holder = serializers.CharField(required=True)
    credit_card_number = serializers.CharField(required=True)
    exp_date = serializers.CharField(required=True)
    card_cvv = serializers.CharField(required=True)
    deposit_amount = serializers.IntegerField(required=True)


class SubscriptionCancelSerializer(serializers.Serializer):
    deactivate = serializers.BooleanField(required=True)


class SubscriptionActivateSerializer(serializers.Serializer):
    activate = serializers.BooleanField(required=True)
