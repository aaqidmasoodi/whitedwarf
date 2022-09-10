from django.db import models
from django.contrib.auth import get_user_model
from buses.models import Bus
from core.settings import SECRET_KEY
from datetime import datetime
import jwt


User = get_user_model()


class PaymentValidationToken(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=600)
    scanned = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token


class SeatReservationStatus(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(
        Bus, default=None, null=True, blank=True, on_delete=models.SET_NULL
    )

    token = models.CharField(max_length=600, null=True, default=None)

    @property
    def status(self):
        return self.get_reservation_status()

    def get_reservation_status(self):
        if not self.token:
            return False
        try:
            jwt.decode(self.token, SECRET_KEY, algorithms=["HS256"])
            return True

        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    @property
    def days_left(self):
        if not self.token:
            return 0

        try:
            payload = jwt.decode(self.token, SECRET_KEY, algorithms=["HS256"])
            expiry = datetime.fromtimestamp(payload["exp"])
            delta_time = expiry - datetime.now()

            days = delta_time.days if delta_time.days >= 1 else 0

            return days

        except jwt.ExpiredSignatureError:
            return 0
        except jwt.InvalidTokenError:
            return 0

    def __str__(self):
        return f"{self.user.name} Reservation Status"


class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True)
    payment_date = models.DateTimeField()
    amount = models.FloatField()

    def __str__(self):
        return f"{self.user.name}-{self.amount}"
