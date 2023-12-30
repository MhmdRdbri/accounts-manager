from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


class CustomUserManager(BaseUserManager):
    # def create_user(self, phone_number, password=None, **extra_fields):
    #     if not phone_number:
    #         raise ValueError("The Phone Number must be set")
    #     user = self.model(phone_number=phone_number, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number must be set")

        profile_data = extra_fields.pop(
            "profile", {}
        )  # Extract profile data if provided
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)

        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(unique=True, max_length=15)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    @property
    def is_admin_user(self):
        return self.is_staff or self.is_superuser or self.is_admin


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    fullname = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    username = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profile of {self.user.phone_number}"
