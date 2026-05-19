from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from banking.models import BankAccount


class TransactionHistoryTests(TestCase):
    def test_transaction_history_shows_newest_first(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner', balance=Decimal('100.00'))
        account.deposit('10.00')
        account.withdraw('5.00')

        response = self.client.get(reverse('banking:transaction_list', args=[account.pk]))

        self.assertEqual(response.status_code, 200)
        transactions = list(response.context['transactions'])
        self.assertEqual(transactions[0].transaction_type, 'WITHDRAWAL')
        self.assertEqual(transactions[1].transaction_type, 'DEPOSIT')