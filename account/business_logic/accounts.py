# from .models import Account_Record, Transaction_Record
from signal import default_int_handler
from account.models import TransactionRecord, AccountRecord, AuditRecord
import abc

class Account:
    def __init__(self, account_id: int):
        self.account_id = account_id
        self._balance = None
        self.account_record = AccountRecord.objects.get(pk=self.account_id)
        self.account_type = self.account_record.account_type


    def calculate_initial_balance(self):
        money_in = sum(
            transaction.amount 
            for transaction in self.account_record.money_in_transactions.all()
        )
        money_out = sum(
            transaction.amount 
            for transaction in self.account_record.money_out_transactions.all()
        )
        return money_in - money_out

    
    @property
    def balance(self):
        if self._balance is None:
            self._balance = self.calculate_initial_balance()
        return self._balance


    @balance.setter
    def balance(self, new_balance):
        new_audit_record = AuditRecord(
            account_record=self.account_record,
            old_balance=self.balance,
            new_balance=new_balance
        )
        new_audit_record.save()
        self._balance = new_balance


    def deposit(self, amount):
        self.process_transaction(
            transaction_type='deposit',
            target=self,
            amount=amount
        )


    def withdraw(self, amount):
        self.process_transaction(
            transaction_type='withdraw',
            source=self,
            amount=amount
        )
        

    def transfer_in(self, amount, source_account_id):
        self.process_transaction(
            transaction_type='transfer',
            source=accounts[source_account_id],
            target=self,
            amount=amount
        )

    
    def process_transaction(self, transaction_type: str, source=None, target=None, amount=0):
        '''
        source and target take the 'Account' class.
        '''
        new_transaction_record = TransactionRecord(
            transaction_type=transaction_type,
            source=source.account_record if source else None,
            target=target.account_record if target else None,
            amount=amount
            )
        new_transaction_record.save()
        if source:
            source.balance -= amount
        if target:
            target.balance += amount


class InterestMixin(abc.ABC):
    def apply_monthly_interest(self, monthly_percentage=0.5):
        interest_amount = round(self.balance * monthly_percentage / 100)

        self.process_transaction(
            transaction_type='interest',
            target=self,
            amount=interest_amount
        )


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

        if account_id not in self._accounts:
            self._accounts[account_id] = self.account_factory(account_id)
        return self._accounts[account_id]
            
                
    # Doesn't work quite yet because an instance of Account is only created once it is first called. 
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
