from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


User = get_user_model()


class PaymentValidationToken(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=600)
    scanned = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token
