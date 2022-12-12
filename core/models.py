from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.html import format_html


class User(AbstractUser):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=300, null=True)
    phone = models.CharField(
        max_length=10,
        null=True,
        validators=[
            MinLengthValidator(10)
        ]
    )
    age = models.CharField(max_length=5, null=True)
    birth_date = models.DateField(null=True)

    def name(self):
        return f"{self.user.first_name} {self.user.last_name}"

