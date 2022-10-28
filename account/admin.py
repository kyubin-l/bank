from re import T
from django.contrib import admin
from .models import account_record, transaction_record, audit_record

admin.site.register(account_record)
admin.site.register(transaction_record)
admin.site.register(audit_record)

# Register your models here.
