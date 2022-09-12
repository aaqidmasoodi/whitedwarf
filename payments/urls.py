from django.urls import path
from . import views


urlpatterns = [
    path(
        "create-payment-intent/",
        views.CreatePaymentIntent.as_view(),
        name="create-payment",
    ),
    path("webhook/", views.PaymentWebhook.as_view(), name="stripe-webhook"),
    path("generate-qr/", views.GenerateQR.as_view(), name="generate-qr"),
    path("validate-qr/", views.ValidateQR.as_view(), name="validate-qr"),
    path("", views.UserPaymentListView.as_view(), name="user-payments"),
]
