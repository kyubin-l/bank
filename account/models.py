from django.db import models
from django.utils import timezone


# Create your models here.

class account_record(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class transaction_record(models.Model):

    transition_record_options = (
        ('deposit', 'DEPOSIT'),
        ('withdrawal', 'WITHDRAWAL'),
        ('transfer', 'TRANSFER')
    )

    transaction_type = models.CharField(max_length=10, choices=transition_record_options)
    source = models.ForeignKey(
        account_record,
        on_delete=models.PROTECT, 
        related_name='money_out_transactions', 
        null=True, 
        blank=True
    )
    target = models.ForeignKey(
        account_record, 
        on_delete=models.PROTECT, 
        related_name='money_in_transactions', 
        null=True, 
        blank=True
    )
    amount = models.IntegerField('amount', default=0)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.transaction_type}, {self.source}, {self.target}, {self.amount}'


class audit_record(models.Model):
    account_record = models.ForeignKey(
        account_record,
        on_delete=models.PROTECT,
    )
    old_balance = models.IntegerField(default=0)
    new_balance = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.account_record}, {self.old_balance}, {self.new_balance}'