from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField("Номер телефона", max_length=15, unique=True)
    email = models.EmailField("Электронная почта", unique=True)

    def __str__(self):
        return self.username