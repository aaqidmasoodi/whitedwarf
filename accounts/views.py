from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from accounts import serializers
from .models import PhoneOTP
from django.contrib.auth import login
from . import utils

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication


class SendOTPView(APIView):
    def post(self, request, *args, **kwargs):

        serializer = serializers.PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:

            phone = serializer.validated_data["phone"]

            # checking if we have already sent an otp to this phone number
            if PhoneOTP.objects.filter(phone__iexact=phone).exists():
                record = PhoneOTP.objects.filter(phone__iexact=phone).first()

                if record.count >= 10:
                    return Response(
                        {
                            "error": "You have exceeded the OTP limit. Please contact support."
                        },
                        status=status.HTTP_409_CONFLICT,
                    )

                otp = utils.send_otp(phone)

                if otp:
                    """
                    Do not try to shorten the code that modifes the count,
                    in many cases it can causes a race condition and yeild
                    unexpected results.
                    """
                    # update the otp count
                    prev_count = record.count
                    record.count = prev_count + 1
                    # update the new otp sent
                    record.otp = otp
                    record.save()
                else:
                    return Response(
                        {"error": "Sending OTP failed. Try again later."},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE,
                    )

            else:
                otp = utils.send_otp(phone)

                if otp:
                    PhoneOTP.objects.create(phone=phone, otp=otp, count=1)

                else:
                    return Response(
                        {"error": "Sending OTP failed. Try again later."},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE,
                    )

            return Response(
                {"detail": f"An OTP was sent sucessfully to +91 {phone}"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ValidateOTP(APIView):
    def post(self, request, *args, **kwargs):

        serializer = serializers.PhoneOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            phone = serializer.validated_data["phone"]
            otp = serializer.validated_data["otp"]
            record = PhoneOTP.objects.filter(phone__iexact=phone).first()

            if str(otp) == str(record.otp):
                record.validated = True
                record.save()
                return Response(
                    {"detail": "The OTP has been verified. Success."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "The OTP didn't match. Try again."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        except Exception as e:
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(KnoxLoginView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        login(request, user)
        return super().post(request, *args, **kwargs)
