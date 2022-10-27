from django.shortcuts import render
from django.views import generic

from .models import Account_Record
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'account/index.html'
    context_object_name = 'all_accounts'

    def get_queryset(self):
        return Account_Record.objects.all()
