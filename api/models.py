from django.contrib.auth.models import User
from django.db import models


class Usuario(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name='user')


class Account(models.Model):
    name = models.CharField(max_length=255)


class Transaction(models.Model):
    description = models.CharField(max_length=255)
    date = models.DateField()
    value = models.DecimalField(max_digits=12, decimal_places=2)
