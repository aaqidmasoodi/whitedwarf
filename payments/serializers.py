from rest_framework import serializers
from .models import PaymentValidationToken
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
            raise serializers.ValidationError("Token has expired. Get a new one.")
        except jwt.InvalidTokenError:
            raise serializers.ValidationError("Token Invalid.")

        return attrs