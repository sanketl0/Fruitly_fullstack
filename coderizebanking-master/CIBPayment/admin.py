from django.contrib import admin

from .models.transaction_status import TransactionStatus
from .models.bank_server_sync import BankServerSync
from .models.transaction_initiation import TransactionInitiation

from .models.account_statement import AccountStatement







admin.site.register(AccountStatement)
admin.site.register(BankServerSync)
admin.site.register(TransactionInitiation)
admin.site.register(TransactionStatus)


