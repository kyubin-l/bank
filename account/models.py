from django.db import models
from django.utils import timezone


# Create your models here.

class AccountRecord(models.Model):
    account_type_options = (
        ('savings', 'SAVINGS'),
        ('current', 'CURRENT'),
        ('super_saving','SUPER_SAVING')
    )
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=15, choices=account_type_options, default='current')

    def __str__(self) -> str:
        return self.name


class TransactionRecord(models.Model):
    transition_record_options = (
        ('deposit', 'DEPOSIT'),
        ('withdrawal', 'WITHDRAWAL'),
        ('transfer', 'TRANSFER'),
        ('interest', 'INTEREST')
    )

    transaction_type = models.CharField(max_length=10, choices=transition_record_options)
    source = models.ForeignKey(
        AccountRecord,
        on_delete=models.PROTECT, 
        related_name='money_out_transactions', 
        null=True, 
        blank=True
    )
    target = models.ForeignKey(
        AccountRecord, 
        on_delete=models.PROTECT, 
        related_name='money_in_transactions', 
        null=True, 
        blank=True
    )
    amount = models.IntegerField('amount', default=0)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.transaction_type}, {self.source}, {self.target}, {self.amount}'


class AuditRecord(models.Model):
    account_record = models.ForeignKey(
        AccountRecord,
        on_delete=models.PROTECT,
    )
    old_balance = models.IntegerField(default=0)
    new_balance = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.account_record}, {self.old_balance}, {self.new_balance}'