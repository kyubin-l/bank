# from .models import Account_Record, Transaction_Record
from account.models import TransactionRecord, AccountRecord, AuditRecord

class Account:
    def __init__(self, account_id):
        self.account_id = account_id
        self._balance = None
        self._account_record = AccountRecord.objects.get(pk=self.account_id)


    def calcuate_initial_balance(self):
        money_in = sum([
            transaction.amount 
            for 
            transaction 
            in 
            self._account_record.money_in_transactions.all()
        ])
        money_out = sum([
            transaction.amount 
            for 
            transaction 
            in 
            self._account_record.money_out_transactions.all()
        ])

        return money_in - money_out

    
    @property
    def balance(self):
        if self._balance is None:
            self._balance = self.calcuate_initial_balance()
        return self._balance


    @balance.setter
    def balance(self, new_balance):
        new_audit_record = AuditRecord(
            account_record = self._account_record,
            old_balance = self.balance,
            new_balance = new_balance
        )
        new_audit_record.save()
        self._balance = new_balance


    def deposit(self, amount):
        self.balance += amount
        new_transaction_record = TransactionRecord(
            transaction_type = 'deposit',
            target = self._account_record,
            amount = amount
        )
        new_transaction_record.save()


    def withdraw(self, amount):
        self.balance -= amount
        new_transaction_record = TransactionRecord(
            transaction_type = 'withdraw',
            source = self._account_record,
            amount = amount
        )
        new_transaction_record.save()
        

    def transfer_in(self, amount, source_account_id):
        self.balance += amount
        accounts[source_account_id].balance -= amount
        new_transaction_record = TransactionRecord(
            transaction_type = 'transfer',
            source = AccountRecord.objects.get(pk=source_account_id),
            target = self._account_record,
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
