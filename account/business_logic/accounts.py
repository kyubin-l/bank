# from .models import Account_Record, Transaction_Record
from django.db.models import Q
from account.models import Transaction_Record, Account_Record

class Account:
    def __init__(self, account_id):
        self.account_id = account_id
        self.balance = 0
        self.calcuate_current_balance()


    def calcuate_current_balance(self):
        all_transactions = Transaction_Record.objects.filter(Q(source=self.account_id) | Q(target=self.account_id))
        for transaction in all_transactions:
            if transaction.transaction_type == 'deposit':
                self.balance += transaction.amount
            elif transaction.transaction_type == 'withdraw':
                self.balance -= transaction.amount
            else:
                if transaction.source == self.account_id:
                    self.balance -= transaction.amount
                else:
                    self.balance += transaction.amount


    def deposit(self, amount):
        self.balance += amount
        new_transaction_record = Transaction_Record(
            transaction_type = 'deposit',
            target = self.account_id,
            amount = amount
        )
        new_transaction_record.save()


    def withdraw(self, amount):
        self.balance -= amount
        new_transaction_record = Transaction_Record(
            transaction_type = 'withdraw',
            source = self.account_id,
            amount = amount
        )
        new_transaction_record.save()
        

    def transfer_in(self, amount, source_account_id):
        self.balance += amount
        accounts[source_account_id].balance -= amount
        new_transaction_record = Transaction_Record(
            transaction_type = 'transfer',
            source = source_account_id,
            target = self.account_id,
            amount = amount
        )
        new_transaction_record.save()


class Accounts:
    def __init__(self):
        self._accounts = {}
        pass


    def __getitem__(self, account_id):
        if account_id in self._accounts.keys():
            return self._accounts[account_id]
        else:
            self._accounts[account_id] = Account(account_id)
            return self._accounts[account_id]

accounts = Accounts()
