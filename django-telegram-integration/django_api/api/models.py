from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField("Электронная почта", unique=True)
    phone_number = models.CharField("Номер телефона", max_length=15, unique=True, blank=True, null=True)
    telegram_id = models.CharField("Telegram ID", max_length=64, blank=True, null=True, unique=True)  # <- Вот оно

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
