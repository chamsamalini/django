from decimal import Decimal

from django.test import TestCase

from banking.forms import DepositForm, WithdrawForm
from banking.models import BankAccount


class DepositFormTests(TestCase):
    def test_rejects_zero_amount(self):
        form = DepositForm(data={'amount': '0'})

        self.assertFalse(form.is_valid())
        self.assertIn('Enter an amount greater than 0.', form.errors['amount'])

    def test_rejects_negative_amount(self):
        form = DepositForm(data={'amount': '-5'})

        self.assertFalse(form.is_valid())
        self.assertIn('Enter an amount greater than 0.', form.errors['amount'])


class WithdrawFormTests(TestCase):
    def setUp(self):
        self.account = BankAccount.objects.create(account_holder_name='Learner', balance=Decimal('50.00'))

    def test_rejects_zero_amount(self):
        form = WithdrawForm(self.account, data={'amount': '0'})

        self.assertFalse(form.is_valid())
        self.assertIn('Enter an amount greater than 0.', form.errors['amount'])

    def test_rejects_overdraft(self):
        form = WithdrawForm(self.account, data={'amount': '60'})

        self.assertFalse(form.is_valid())
        self.assertIn('Withdrawal rejected because the amount exceeds the available balance.', form.errors['amount'])