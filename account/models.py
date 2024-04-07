from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F
from django.db.models.fields.generated import GeneratedField
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, default="@me.mcu.edu.tw")

    full_name = GeneratedField(
        verbose_name=_("full name"),
        expression=Concat(
            F("last_name"),
            F("first_name"),
            output_field=models.CharField(max_length=16),
        ),
        output_field=models.CharField(max_length=16),
        db_persist=True,
    )

    def __str__(self):
        return self.username
