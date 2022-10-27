# from .models import Account_Record, Transaction_Record

from account.models import Transaction_Record, Account_Record

class Account:
    def __init__(self, account_id):
        self.account_id = account_id
        self.balance = 0
        self.calculate_current_balance()


    def calculate_current_balance(self):
        all_transactions = Transaction_Record.objects.all()
        for transaction in all_transactions:
            pass
        pass


    def deposit(self):
        pass


    def withdrawal(self):
        pass


    def transfer_in(self):
        pass



class Accounts:
    def __init__(self):
        self._accounts = {}
        pass


    def __getitem__(self, account_id):
        if self._accounts[account_id]:
            return self._accounts[account_id]
        else:
            self._accounts[account_id] = Account(account_id)
            return self._accounts[account_id]


            
    




        


accounts = Accounts()
