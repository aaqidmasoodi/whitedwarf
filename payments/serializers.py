from dataclasses import field
from rest_framework import serializers
from .models import Payment, PaymentValidationToken, SeatReservationStatus
from core.settings import SECRET_KEY
from django.contrib.auth import get_user_model
from buses.models import Bus
import jwt


User = get_user_model()


class PaymentValidationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentValidationToken
        fields = ["user", "token"]


class TokenSerializer(serializers.Serializer):

    token = serializers.CharField(max_length=600)

    def validate(self, attrs):
        token = attrs.get("token")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            attrs["payload"] = payload

        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError(
                "This QR Code has expired. Generate a new one."
            )
        except jwt.InvalidTokenError:
            raise serializers.ValidationError("Invalid QR Code.")

        return attrs


class SeatReservationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatReservationStatus
        fields = [
            "status",
            "days_left",
            "expiry_date",
        ]


# this one is used to serialize the users last payment with minimal information
class LastPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["payment_date", "amount"]


"""
    PAYMENT LIST SERIALIZERS START
    ++++++++++++++++++++++++++++++
"""

# this serializer is used to expand the user field in on the payment object
class PaymentUserFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name"]


class PaymentBusFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ["number"]


# this one i have used to provide detailed info about the payments in llst view
class PaymentSerializer(serializers.ModelSerializer):
    user = PaymentUserFieldSerializer()
    bus = PaymentBusFieldSerializer()

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "bus",
            "payment_date",
            "amount",
            "payment_method",
            "transaction_id",
            "card_brand",
            "card_last4",
        ]


"""
    ++++++++++++++++++++++++++++
    PAYMENT LIST SERIALIZERS END
"""
