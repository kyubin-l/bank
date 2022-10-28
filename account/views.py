from re import A
from django.shortcuts import render
from django.views import generic
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse
from .business_logic.accounts import accounts



from .models import AccountRecord, TransactionRecord
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'account/index.html'
    context_object_name = 'all_accounts'

    def get_queryset(self):
        return AccountRecord.objects.all()


def withdraw(request):
    if request.method == 'GET':
        all_accounts = AccountRecord.objects.all()
        return render(request, 'account/withdraw.html', {'all_accounts': all_accounts})

    elif request.method == 'POST':
        account_id  = request.POST['account_id']
        amount  = int(request.POST['amount'])

        accounts[account_id].withdraw(amount)

        messages.success(request, f'You succesfully withdrew {amount} from account \
            {AccountRecord.objects.get(pk=account_id)}')
        messages.success(request, f'Account balance for \
            {AccountRecord.objects.get(pk=account_id)}: {accounts[account_id].balance}')

    return HttpResponseRedirect(reverse('withdraw'))


def deposit(request):
    if request.method == 'GET':
        all_accounts = AccountRecord.objects.all()
        return render(request, 'account/deposit.html', {'all_accounts': all_accounts})

    elif request.method == 'POST':
        account_id  = request.POST['account_id']
        amount  = int(request.POST['amount'])

        accounts[account_id].deposit(amount)

        messages.success(request, f'You succesfully deposited {amount} to account \
            {AccountRecord.objects.get(pk=account_id)}')
        messages.success(request, f'Account balance for \
            {AccountRecord.objects.get(pk=account_id)}: {accounts[account_id].balance}')

    return HttpResponseRedirect(reverse('deposit'))


def transfer(request):
    if request.method == 'GET':
        all_accounts = AccountRecord.objects.all()
        return render(request, 'account/transfer.html', {'all_accounts': all_accounts})

    elif request.method == 'POST':
        source_account_id  = request.POST['source_account_id']
        target_account_id = request.POST['target_account_id']
        amount  = int(request.POST['amount'])

        accounts[target_account_id].transfer_in(amount, source_account_id)

        messages.success(request, f'You succesfully transfered {amount} from account \
            {AccountRecord.objects.get(pk=source_account_id)} \
            to account {AccountRecord.objects.get(pk=target_account_id)}')
        messages.success(request, f'Account balance for \
            {AccountRecord.objects.get(pk=source_account_id)}: {accounts[source_account_id].balance}') 
        messages.success(request, f'Account balance for \
            {AccountRecord.objects.get(pk=target_account_id)}: {accounts[target_account_id].balance}') 

    return HttpResponseRedirect(reverse('transfer'))
    

def monthly_interest(request):
    savings_account_records = AccountRecord.objects.filter(account_type='savings')
    saving_accounts = [accounts[account.id] for account in savings_account_records]

    if request.method == 'GET':
        return render(request, 'account/monthly_interest.html', {'saving_accounts': saving_accounts})
    
    elif request.method == 'POST':
        interest_rate = float(request.POST['interest'])
        account_id = request.POST['account_id']
        accounts[account_id].apply_monthly_interest(monthly_percentage=interest_rate)
        return render(request, 'account/monthly_interest.html', {'saving_accounts': saving_accounts})

