from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.db.models.functions import Concat
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext as _

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "full_name", "email", "is_staff"]
    search_fields = ["username", "full_name"]
