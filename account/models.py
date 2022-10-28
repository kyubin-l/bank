from django.db import models
from django.utils import timezone


# Create your models here.

class Account_Record(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Transaction_Record(models.Model):

    transition_record_options = (
        ('deposit', 'DEPOSIT'),
        ('withdrawal', 'WITHDRAWAL'),
        ('transfer', 'TRANSFER')
    )
    transaction_type = models.CharField(max_length=10, choices=transition_record_options)
    source = models.IntegerField(null=True, blank=True)
    target = models.IntegerField(null=True, blank=True)
    amount = models.IntegerField('amount', default=0)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.transaction_type}'
