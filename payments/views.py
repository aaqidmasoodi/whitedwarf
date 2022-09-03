import os
from dotenv import load_dotenv
import json
import stripe
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from .models import PaymentValidationToken
from .serializers import PaymentValidationTokenSerializer
from payments import serializers
from . import utils
from django.contrib.auth import get_user_model
from accounts.serializers import UserPublicSerializer


User = get_user_model()


load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")


class CreatePaymentIntent(APIView):
    def post(self, request, *args, **kwargs):

        print("using this...")

        try:
            intent = stripe.PaymentIntent.create(
                amount=140000,
                currency="INR",
                automatic_payment_methods={
                    "enabled": True,
                },
            )
            return Response({"clientSecret": intent["client_secret"]})
        except Exception as e:
            return Response({"error": str(e)})


class PaymentWebhook(APIView):
    def post(self, request, *args, **kwargs):
        event = None
        payload = request.body

        try:
            event = json.loads(payload)
        except Exception as e:
            print("Webhook error while parsing basic request." + str(e))
            return Response({"success": False})

        if endpoint_secret:
            sig_header = request.headers.get("stripe-signature")
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, endpoint_secret
                )

                # print(event)
            except stripe.error.SignatureVerificationError as e:
                print("Webhook signature verification failed." + str(e))
                return Response({"success": False})

        # Handle the events

        if event["type"] == "payment_intent.created":
            print("Payment Intent was created sucessfully.")

        elif event and event["type"] == "payment_intent.succeeded":
            payment_intent = event["data"]["object"]  # contains a stripe.PaymentIntent
            print("Payment for {} succeeded".format(payment_intent["amount"]))

            # fullfillment
            # Then define and call a method to handle the successful payment intent.
            # handle_payment_intent_succeeded(payment_intent)
        else:
            # Unexpected event type
            print("Unhandled event type {}".format(event["type"]))

        return Response({"success": True})


class GenerateQR(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        QR_TYPE = "CUKBRS"
        user = request.user
        token = utils.generate_token(user.phone)
        qr_payload = f"{QR_TYPE}?{token}"

        if PaymentValidationToken.objects.filter(user=user.id).exists():
            record = PaymentValidationToken.objects.filter(user=user.id).first()
            record.token = qr_payload
            record.scanned = False
            record.save()
        else:
            serializer = PaymentValidationTokenSerializer(
                data={"user": user.id, "token": qr_payload}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response({"payload": qr_payload}, status=status.HTTP_200_OK)


class ValidateQR(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = serializers.TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        userPhone = serializer.validated_data["payload"]["user"]
        user = User.objects.filter(phone__iexact=userPhone).first()
        serializer = UserPublicSerializer(user)

        try:
            record = PaymentValidationToken.objects.get(user=user.id)
            if record.scanned:
                return Response(
                    {"non_field_errors": ["This QR Code has already been scanned."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                record.scanned = True
                record.save()
        except PaymentValidationToken.DoesNotExist:
            return Response(
                {
                    "non_field_errors": [
                        "Could not validate this QR Code. Try generating a new one."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"data": serializer.data}, status=status.HTTP_202_ACCEPTED)
