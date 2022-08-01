import os
from dotenv import load_dotenv
import json
import stripe

from rest_framework.decorators import api_view
from rest_framework.response import Response

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")


@api_view(["POST"])
def create_payment(request):
    try:
        # data = json.loads(request.body)
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


@api_view(["POST"])
def webhook(request):
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
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

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
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)

    elif event["type"] == "charge.succeeded":
        print("Charge suceeded!.")

    elif event["type"] == "payment_method.attached":
        payment_method = event["data"]["object"]  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    else:
        # Unexpected event type
        print("Unhandled event type {}".format(event["type"]))

    return Response({"success": True})
