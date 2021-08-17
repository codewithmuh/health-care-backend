from django.urls import path

from subscription.views import SubscriptionCard, SubscriptionCancel, SubscriptionActivate

urlpatterns = [
    path('subscription/', SubscriptionCard.as_view(), name='subscription'),
    path('subscription-cancel/', SubscriptionCancel.as_view(), name='subscription_cancel'),
    path('subscription-activate/', SubscriptionActivate.as_view(), name='subscription_activate'),
]
