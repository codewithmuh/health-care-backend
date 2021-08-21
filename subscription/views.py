from datetime import timedelta

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from djstripe.models import Plan, Subscription, Customer, PaymentMethod
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from subscription.serializers import CardDetailSerializer

stripe.api_key = settings.STRIPE_API_KEY
User = get_user_model()


class SubscriptionCard(ListCreateAPIView):
    serializer_class = CardDetailSerializer
    queryset = User.objects.none

    def get(self, request, *args, **kwargs):
        return Response()

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            serializer = CardDetailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            try:
                token = stripe.Token.create(
                    card={
                        "number": data.get("card_number"),
                        "exp_month": data.get("card_exp_month"),
                        "exp_year": data.get("card_exp_year"),
                        "cvc": data.get("card_cvv")
                    }, )
                try:
                    customer = Customer.objects.filter(subscriber=request.user).first()
                except Customer.DoesNotExist:
                    customer = Customer.create(subscriber=request.user)
                    customer.save()
                print(customer.default_payment_method)
                try:
                    payment_method = stripe.PaymentMethod.create(
                        type="card",
                        card={"token": token.id},
                    )
                    card = customer.add_payment_method(
                        payment_method=payment_method.id, set_default=True)
                    customer.api_retrieve()
                except stripe.error.CardError as e:
                    print(e)
                try:
                    pi = stripe.PaymentIntent.create(
                        amount=int(data.get("amount")),
                        currency="usd",
                        payment_method_types=["card"],
                        customer=customer.id,
                        description='Added cash',
                    )
                    stripe.PaymentIntent.confirm(
                        pi.id,
                        payment_method=customer.payment_methods.first().id,
                    )
                    if pi.id:
                        try:
                            credits_purchased = (data.get("amount") / 100) * 4
                            user.credits += credits_purchased
                            user.save()
                        except Exception as e:
                            print(e)
                    return Response(status=status.HTTP_200_OK, data={
                        "ok": True,
                        "error": None,
                        "amount": user.credits
                    })
                except Exception as err:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={
                        "ok": False,
                        "error": str(err),
                    })
            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    "ok": False,
                    "error": err.get('type'),
                    "message": err.get('message')
                })
            except Exception as e:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={
                    "ok": False,
                    "error": "Server Error",
                    "message": "Invalid Card Detail"
                })
        return Response({"error": "Please login first."}, status=status.HTTP_403_FORBIDDEN)
