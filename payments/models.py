from django.db import models
from django.contrib.auth import get_user_model
from buses.models import Bus


User = get_user_model()


class PaymentValidationToken(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=600)
    scanned = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token


class SeatReservation(models.Model):

    RESERVATION_CHOICES = [
        ("E", "EXPIRED"),
        ("A", "ACTIVE"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=RESERVATION_CHOICES, default="E")
    token = models.CharField(max_length=600)


class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    bus = models.ForeignKey(Bus, on_delete=models.DO_NOTHING)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
