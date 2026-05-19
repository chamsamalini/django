from decimal import Decimal

from django import forms

from .models import BankAccount


class BankAccountCreateForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_holder_name']


class AmountForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        error_messages={'required': 'Enter an amount greater than 0.', 'invalid': 'Enter a valid number.'},
    )

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= Decimal('0.00'):
            raise forms.ValidationError('Enter an amount greater than 0.')
        return amount


class DepositForm(AmountForm):
    pass


class WithdrawForm(AmountForm):
    def __init__(self, account, *args, **kwargs):
        self.account = account
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = super().clean_amount()
        if amount > self.account.balance:
            raise forms.ValidationError('Withdrawal rejected because the amount exceeds the available balance.')
        return amount