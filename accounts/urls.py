from django.urls import path
from . import views


urlpatterns = [
    path("send-otp/", views.SendOTPView.as_view(), name="send-otp"),
    path("validate-otp/", views.ValidateOTP.as_view(), name="validate-otp"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("user-info/", views.UserInfoView.as_view(), name="user-info"),
]
