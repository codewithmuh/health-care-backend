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
from subscription.serializers import CardDetailSerializer, SubscriptionCancelSerializer, SubscriptionActivateSerializer

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
                        "card_holder": data.get("card_holder"),
                        "number": data.get("credit_card_number"),
                        "exp_date": data.get("exp_date"),
                        "cvc": data.get("card_cvv"),
                        "deposit_amount": data.get("deposit_amount")
                    }, )
                try:
                    customer = Customer.objects.filter(subscriber=request.user).first()
                except Customer.DoesNotExist:
                    customer = Customer.create(subscriber=request.user)
                    customer.save()
                    customer.api_retrieve()
                print(customer.default_payment_method)
                try:
                    payment_method = stripe.PaymentMethod.create(
                        type="card",
                        card={"token": token.id},
                    )
                    card = customer.add_payment_method(
                        payment_method=payment_method.id, set_default=True)
                    print(card)
                except stripe.error.CardError as e:
                    print(e)
                # try:
                #     old_payment_methods = customer.payment_methods.filter(~Q(id=customer.default_payment_method.id))
                #     # print(old_payment_methods)
                #     old_payment_methods.delete()
                #
                # except PaymentMethod.DoesNotExist:
                #     pass

                plan = Plan.objects.first()
                if plan:
                    arguments = {
                        "customer": customer.id,
                        "items": [
                            {
                                "plan": plan.id,
                            },
                        ]
                    }
                    subscription = stripe.Subscription.create(**arguments)
                    user.subscription_id = subscription.id
                    user.is_subscription_active = True
                    user.card_number = f"**** **** **** {data.get('credit_card_number')[-4:]}"
                    now = timezone.now().date()
                    user.renew_date = now
                    if plan.trial_period_days:
                        user.renew_date = now + timedelta(days=plan.trial_period_days)
                    user.save()
                return Response(status=status.HTTP_200_OK, data={
                    "ok": True,
                    "error": None,
                    "message": "Created"
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


class SubscriptionCancel(ListCreateAPIView):
    serializer_class = SubscriptionCancelSerializer
    queryset = User.objects.none

    def get(self, request, *args, **kwargs):
        return Response()

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            stripe_customer = Customer.objects.filter(subscriber=user).first()

            if stripe_customer:
                try:
                    stripe.Subscription.modify(
                        user.subscription_id,
                        cancel_at_period_end=True
                    )
                    user.is_subscription_active = False
                    user.save()
                    return Response(status=status.HTTP_200_OK, data={
                        "ok": True,
                        "error": None,
                    })
                except Exception as err:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={
                        "ok": False,
                        "error": str(err),
                    })
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data={
                    "ok": False,
                    "error": "Customer Does not exist.",
                })
        return Response({"error": "Please login first."}, status=status.HTTP_403_FORBIDDEN)


class SubscriptionActivate(ListCreateAPIView):
    serializer_class = SubscriptionActivateSerializer
    queryset = User.objects.none

    def get(self, request, *args, **kwargs):
        return Response()

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            stripe_customer = Customer.objects.get(subscriber=user)

            if stripe_customer:
                try:
                    stripe.Subscription.modify(
                        user.subscription_id,
                        cancel_at_period_end=False
                    )
                    user.is_subscription_active = True
                    user.save()
                    return Response(status=status.HTTP_200_OK, data={
                        "ok": True,
                        "error": None,
                    })
                except Exception as err:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={
                        "ok": False,
                        "error": str(err),
                    })
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data={
                    "ok": False,
                    "error": "Customer Does not exist.",
                })
        return Response({"error": "Please login first."}, status=status.HTTP_403_FORBIDDEN)


