from django.db import models
from accounts.models import User


# New Buses will be added using the admin site
class Bus(models.Model):
    number = models.PositiveBigIntegerField()
    plate_number = models.CharField(max_length=255, default=0)
    seats = models.PositiveBigIntegerField()
    current_driver = models.ForeignKey(
        "Driver", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):

        return f"Bus {self.number} - {self.plate_number}"

    class Meta:
        verbose_name_plural = "Buses"


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_bus = models.ForeignKey("Bus", on_delete=models.SET_NULL, null=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alloted_bus = models.ForeignKey("Bus", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.name
