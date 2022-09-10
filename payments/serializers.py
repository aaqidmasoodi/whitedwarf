from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from .models import PaymentValidationToken, SeatReservationStatus
from core.settings import SECRET_KEY
from datetime import datetime, timedelta
import jwt


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
        ]
