from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# import jsonfield

from .managers import CustomUserManager


DIET_CHOICES = (
    (-1, '다이어트'),
    (0, '유지'),
    (1, '증량')
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    nickname = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)
    diet = models.SmallIntegerField(choices=DIET_CHOICES, null=True, blank=True)
    allergy = models.JSONField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['nickname',]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_nickname(self):
        return self.nickname