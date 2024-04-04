from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(_("email address"), blank=True, default="@me.mcu.edu.tw")

    def __str__(self):
        return self.username
