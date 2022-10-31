# from .models import Account_Record, Transaction_Record
from signal import default_int_handler
from account.models import TransactionRecord, AccountRecord, AuditRecord

class Account:
    def __init__(self, account_id: int):
        self.account_id = account_id
        self._balance = None
        self.account_record = AccountRecord.objects.get(pk=self.account_id)
        self.account_type = self.account_record.account_type


    def calculate_initial_balance(self):
        money_in = sum([
            transaction.amount 
            for 
            transaction 
            in 
            self.account_record.money_in_transactions.all()
        ])
        money_out = sum([
            transaction.amount 
            for 
            transaction 
            in 
            self.account_record.money_out_transactions.all()
        ])

        return money_in - money_out

    
    @property
    def balance(self):
        if self._balance is None:
            self._balance = self.calculate_initial_balance()
        return self._balance


    @balance.setter
    def balance(self, new_balance):
        new_audit_record = AuditRecord(
            account_record = self.account_record,
            old_balance = self.balance,
            new_balance = new_balance
        )
        new_audit_record.save()
        self._balance = new_balance


    def deposit(self, amount):
        self.balance += amount
        new_transaction_record = TransactionRecord(
            transaction_type = 'deposit',
            target = self.account_record,
            amount = amount
        )
        new_transaction_record.save()


    def withdraw(self, amount):
        self.balance -= amount
        new_transaction_record = TransactionRecord(
            transaction_type = 'withdraw',
            source = self.account_record,
            amount = amount
        )
        new_transaction_record.save()
        

    def transfer_in(self, amount, source_account_id):
        self.balance += amount
        accounts[source_account_id].balance -= amount
        new_transaction_record = TransactionRecord(
            transaction_type = 'transfer',
            source = AccountRecord.objects.get(pk=source_account_id),
            target = self.account_record,
            amount = amount
        )
        new_transaction_record.save()


class InterestMixin:
    def apply_monthly_interest(self, monthly_percentage=0.5):
        interest_amount = round(self.balance * monthly_percentage / 100)
        self.balance += interest_amount

        new_transaction_record = TransactionRecord(
            transaction_type = 'interest',
            target = self.account_record,
            amount = interest_amount
        )
        new_transaction_record.save()


class SavingsAccount(Account, InterestMixin):
    account_type = 'savings'        
    default_interest_rate = 0.5


class SuperSavingsAccount(Account, InterestMixin):
    account_type = 'super_saving'
    default_interest_rate = 0.7


class Accounts:
    def __init__(self):
        self._accounts = {}
        self._savings_accounts = []
        pass

    def account_factory(self, account_id):
        account_type = AccountRecord.objects.get(pk=account_id).account_type
        if account_type == 'current':
            return Account(account_id)
        elif account_type == 'savings':
            return SavingsAccount(account_id)
        else:
            return SuperSavingsAccount(account_id)


    def __getitem__(self, account_id: int):
        assert type(account_id) == int

        if account_id in self._accounts.keys():
            return self._accounts[account_id]
        else:
            self._accounts[account_id] = self.account_factory(account_id)
                
        return self._accounts[account_id]


    # @property
    # def savings_accounts(self) -> list:
    #     savings_account_types = ['savings', 'super_saving']
    #     self._savings_accounts = [
    #         account for account in self._accounts.values()
    #         if 
    #         account.account_type 
    #         in
    #         savings_account_types
    #     ]
    #     return self._savings_accounts


accounts = Accounts()
