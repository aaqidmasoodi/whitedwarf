from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from buses.models import Bus


class UserManager(BaseUserManager):
    def create_user(self, phone, name, password=None, password2=None):
        if not phone:
            raise ValueError("Users must have a phone number")

        user = self.model(
            phone=phone,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password=None):
        user = self.create_user(phone=phone, name=name, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    bus = models.ForeignKey(
        Bus, on_delete=models.SET_NULL, default=None, null=True, blank=True
    )

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_driver = models.BooleanField(default=False)
    is_coordinator = models.BooleanField(default=False)
    is_first_login = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        default="profile_pictures/default.png", upload_to="profile_pictures"
    )

    def __str__(self):

        return f"{self.user.name} Profile"


class PhoneOTP(models.Model):
    phone = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=4, blank=True, null=True)
    count = models.IntegerField(default=0, help_text="Number of OTPs sent")
    validated = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP {self.otp} sent to {self.phone}"
