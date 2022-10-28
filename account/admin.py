from re import T
from django.contrib import admin
from .models import AccountRecord, TransactionRecord, AuditRecord

admin.site.register(AccountRecord)
admin.site.register(TransactionRecord)
admin.site.register(AuditRecord)

# Register your models here.
