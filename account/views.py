from django.shortcuts import render
from django.views import generic
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse
from .business_logic.accounts import accounts



from .models import Account_Record, Transaction_Record
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'account/index.html'
    context_object_name = 'all_accounts'

    def get_queryset(self):
        return Account_Record.objects.all()


def withdraw(request):
    if request.method == 'GET':
        all_accounts = Account_Record.objects.all()
        return render(request, 'account/withdraw.html', {'all_accounts': all_accounts})

    elif request.method == 'POST':
        account_id  = request.POST['account_id']
        amount  = int(request.POST['amount'])

        accounts[account_id].withdraw(amount)

        messages.success(request, f'You succesfully withdrew {amount} from account \
            {Account_Record.objects.get(pk=account_id)}')
        messages.success(request, f'Account balance for \
            {Account_Record.objects.get(pk=account_id)}: {accounts[account_id].balance}')

    return HttpResponseRedirect(reverse('withdraw'))


def deposit(request):
    if request.method == 'GET':
        all_accounts = Account_Record.objects.all()
        return render(request, 'account/deposit.html', {'all_accounts': all_accounts})

    elif request.method == 'POST':
        account_id  = request.POST['account_id']
        amount  = int(request.POST['amount'])

        accounts[account_id].deposit(amount)

        messages.success(request, f'You succesfully deposited {amount} to account \
            {Account_Record.objects.get(pk=account_id)}')
        messages.success(request, f'Account balance for \
            {Account_Record.objects.get(pk=account_id)}: {accounts[account_id].balance}')

    return HttpResponseRedirect(reverse('deposit'))


def transfer(request):
    if request.method == 'GET':
        all_accounts = Account_Record.objects.all()
        return render(request, 'account/transfer.html', {'all_accounts': all_accounts})

    elif request.method == 'POST':
        source_account_id  = request.POST['source_account_id']
        target_account_id = request.POST['target_account_id']
        amount  = int(request.POST['amount'])

        accounts[target_account_id].transfer_in(amount, source_account_id)

        messages.success(request, f'You succesfully transfered {amount} from account \
            {Account_Record.objects.get(pk=source_account_id)} \
            to account {Account_Record.objects.get(pk=target_account_id)}')
        messages.success(request, f'Account balance for \
            {Account_Record.objects.get(pk=source_account_id)}: {accounts[source_account_id].balance}') 
        messages.success(request, f'Account balance for \
            {Account_Record.objects.get(pk=target_account_id)}: {accounts[target_account_id].balance}') 

    return HttpResponseRedirect(reverse('transfer'))
    
