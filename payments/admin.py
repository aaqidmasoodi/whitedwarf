from django.contrib import admin
from .models import PaymentValidationToken, SeatReservationStatus, Payment


@admin.register(PaymentValidationToken)
class PaymentValidationTokenAdmin(admin.ModelAdmin):

    readonly_fields = ["user", "token", "scanned"]


@admin.register(SeatReservationStatus)
class SeatReservationStatusAdmin(admin.ModelAdmin):

    readonly_fields = ["user", "bus", "token"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    readonly_fields = [
        "user",
        "bus",
        "payment_date",
        "amount",
        "payment_method",
        "transaction_id",
        "card_brand",
        "card_last4",
    ]
