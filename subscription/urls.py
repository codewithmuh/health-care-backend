from django.urls import path

from subscription.views import SubscriptionCard

urlpatterns = [
    path('purchase/', SubscriptionCard.as_view(), name='subscription'),
]
