from django.db import models

# from django.contrib.auth import get_user_model


# User = get_user_model()

# New Buses will be added using the admin site
class Bus(models.Model):
    number = models.PositiveIntegerField(unique=True)
    plate_number = models.CharField(max_length=255, unique=True)
    seats = models.PositiveIntegerField()
    start = models.CharField(max_length=1024)
    destination = models.CharField(max_length=1024)
    fee = models.FloatField(default=0.00)
    location_broadcast_id = models.CharField(max_length=12, unique=True, blank=True)

    @property
    def reserved_seats(self):
        reservations = list(self.seatreservationstatus_set.all())
        return len([active for active in reservations if active.status == True])

    def save(self, *args, **kwargs):
        self.location_broadcast_id = f"CUKBRS00{self.number}"
        super().save()

    def __str__(self):

        return f"Bus {self.number}"

    class Meta:
        verbose_name_plural = "Buses"


class Alert(models.Model):
    title = models.CharField(max_length=1024)
    body = models.TextField(max_length=2000)

    created_at = models.DateTimeField(auto_now_add=True)

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
