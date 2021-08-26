from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    telegram_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.username)