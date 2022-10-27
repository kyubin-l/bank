from re import T
from django.contrib import admin
from .models import Account_Record, Transaction_Record

admin.site.register(Account_Record)
admin.site.register(Transaction_Record)

# Register your models here.
