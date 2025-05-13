import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from emauth.managers import UserManager


class User(AbstractUser):
    id = models.UUIDField(_("id"), primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(_("email address"), unique=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.full_name} - {self.email}"
