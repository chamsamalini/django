from django.contrib import admin

from .models import BankAccount, Transaction


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
	list_display = ('account_holder_name', 'account_number', 'balance', 'created_at')
	search_fields = ('account_holder_name', 'account_number')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = ('bank_account', 'transaction_type', 'amount', 'created_at')
	list_filter = ('transaction_type',)
