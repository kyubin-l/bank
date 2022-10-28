# from .models import Account_Record, Transaction_Record
from account.models import Transaction_Record, Account_Record

class Account:
    def __init__(self, account_id):
        self.account_id = account_id
        self.calcuate_current_balance()


    def calcuate_current_balance(self):
        account = Account_Record.objects.get(pk=self.account_id)
        money_in = sum([
            transaction.amount 
            for 
            transaction 
            in 
            account.money_in_transactions.all()
        ])
        money_out = sum([
            transaction.amount 
            for 
            transaction 
            in 
            account.money_out_transactions.all()
        ])

        self.balance = money_in - money_out


    def deposit(self, amount):
        self.balance += amount
        new_transaction_record = Transaction_Record(
            transaction_type = 'deposit',
            target = Account_Record.objects.get(pk=self.account_id),
            amount = amount
        )
        new_transaction_record.save()


    def withdraw(self, amount):
        self.balance -= amount
        new_transaction_record = Transaction_Record(
            transaction_type = 'withdraw',
            source = Account_Record.objects.get(pk=self.account_id),
            amount = amount
        )
        new_transaction_record.save()
        

    def transfer_in(self, amount, source_account_id):
        self.balance += amount
        accounts[source_account_id].balance -= amount
        new_transaction_record = Transaction_Record(
            transaction_type = 'transfer',
            source = Account_Record.objects.get(pk=source_account_id),
            target = Account_Record.objects.get(pk=self.account_id),
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
