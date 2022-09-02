from dataclasses import field
from rest_framework import serializers
from accounts.models import User, PhoneOTP, Profile
from django.contrib.auth import authenticate
from buses.serializers import BusSerializer


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10, required=True)

    def validate(self, attrs):

        if User.objects.filter(phone__iexact=attrs.get("phone")).exists():
            raise serializers.ValidationError(
                "A user with that phone number already exists!"
            )

        return attrs


class PhoneOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10, required=True)
    otp = serializers.CharField(max_length=4, required=True)

    def validate(self, attrs):

        if not PhoneOTP.objects.filter(phone__iexact=attrs.get("phone")).exists():
            raise serializers.ValidationError(
                "Unrecognised phone number. Please request a new OTP on this number."
            )

        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "name", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):

        if User.objects.filter(phone__iexact=attrs.get("phone")).exists():
            raise serializers.ValidationError(
                "A user with that phone number already exists!"
            )

        record = PhoneOTP.objects.filter(phone__iexact=attrs.get("phone"))

        if not record.exists():
            raise serializers.ValidationError(
                "You must validate your phone number before registering a new account."
            )

        if not record.first().validated:
            raise serializers.ValidationError(
                "You must validate your phone number before registering a new account."
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)
    password = serializers.CharField(
        max_length=255,
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):

        user = authenticate(
            self.context.get("request"),
            phone=attrs.get("phone"),
            password=attrs.get("password"),
        )

        if not user:

            raise serializers.ValidationError(
                "Could not validate credentials. Try again!"
            )

        attrs.update({"user": user})

        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["profile_picture"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    bus = BusSerializer()

    class Meta:
        model = User
        fields = ["id", "phone", "name", "profile", "bus"]


# will be used to send details about the user along with the payment information
class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "name"]
