from django.urls import path

from subscription.views import PurchaseCredits

urlpatterns = [
    path('purchase/', PurchaseCredits.as_view(), name='purchase_credits'),
]
