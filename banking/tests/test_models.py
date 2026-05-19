from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from banking.models import BankAccount, Transaction


class BankAccountModelTests(TestCase):
    def test_account_creation_starts_with_zero_balance_and_generated_number(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner')

        self.assertEqual(account.balance, Decimal('0.00'))
        self.assertTrue(account.account_number.startswith('ACC-'))

    def test_successful_deposit_updates_balance_and_creates_transaction(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner')

        transaction = account.deposit('25.50')
        account.refresh_from_db()

        self.assertEqual(account.balance, Decimal('25.50'))
        self.assertEqual(transaction.transaction_type, Transaction.TransactionType.DEPOSIT)
        self.assertEqual(account.transactions.count(), 1)

    def test_successful_withdrawal_updates_balance_and_creates_transaction(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner', balance=Decimal('50.00'))

        transaction = account.withdraw('20.00')
        account.refresh_from_db()

        self.assertEqual(account.balance, Decimal('30.00'))
        self.assertEqual(transaction.transaction_type, Transaction.TransactionType.WITHDRAWAL)
        self.assertEqual(account.transactions.count(), 1)

    def test_overdraft_rejection_keeps_balance_non_negative_and_creates_no_transaction(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner', balance=Decimal('40.00'))

        with self.assertRaisesMessage(ValidationError, 'Withdrawal rejected because the amount exceeds the available balance.'):
            account.withdraw('45.00')

        account.refresh_from_db()
        self.assertEqual(account.balance, Decimal('40.00'))
        self.assertEqual(account.transactions.count(), 0)

    def test_invalid_deposit_creates_no_transaction(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner')

        with self.assertRaisesMessage(ValidationError, 'Enter an amount greater than 0.'):
            account.deposit('0')

        self.assertEqual(account.transactions.count(), 0)