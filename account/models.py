from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, default="@me.mcu.edu.tw")

    @property
    def full_name(self):
        return self.last_name + self.first_name

    def __str__(self):
        return self.username
