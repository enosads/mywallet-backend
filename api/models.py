from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Usuario(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name='usuario')


class Account(models.Model):
    name = models.CharField(max_length=255)
    usuario = models.ForeignKey(
        Usuario, models.CASCADE, related_name='accounts')

    def total(self, ):
        transactions = Transaction.objects.filter(
            account=self)
        total = 0
        for transaction in transactions:
            total += transaction.value
        return total

    def income(self, ):
        transactions = Transaction.objects.filter(
            account=self, value__gt=Decimal('0.00'))
        income = 0
        for transaction in transactions:
            income += transaction.value
        return income

    def outcome(self, ):
        transactions = Transaction.objects.filter(
            account=self, value__lt=Decimal('0.00'))
        outcome = 0
        for transaction in transactions:
            outcome += transaction.value
        return outcome


class Transaction(models.Model):
    description = models.CharField(max_length=255)
    date = models.DateField()
    value = models.DecimalField(max_digits=12, decimal_places=2)
    account = models.ForeignKey(
        Account, models.CASCADE, related_name='transactions')
