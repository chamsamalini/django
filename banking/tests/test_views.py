from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from banking.models import BankAccount


class BankingViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('banking:home'))

        self.assertEqual(response.status_code, 200)

    def test_valid_account_creation_redirects_to_detail(self):
        response = self.client.post(reverse('banking:account_create_submit'), {'account_holder_name': 'Workshop Learner'})

        account = BankAccount.objects.get()
        self.assertRedirects(response, reverse('banking:account_detail', args=[account.pk]))

    def test_account_detail_page_shows_balance_data(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner', balance=Decimal('25.00'))

        response = self.client.get(reverse('banking:account_detail', args=[account.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '25.00')
        self.assertContains(response, account.account_number)

    def test_successful_deposit_sets_message_and_updates_balance(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner')

        response = self.client.post(reverse('banking:deposit_submit', args=[account.pk]), {'amount': '20.00'}, follow=True)

        account.refresh_from_db()
        self.assertEqual(account.balance, Decimal('20.00'))
        self.assertContains(response, 'Deposit completed successfully.')

    def test_invalid_deposit_renders_inline_error(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner')

        response = self.client.post(reverse('banking:deposit_submit', args=[account.pk]), {'amount': '0'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter an amount greater than 0.')

    def test_successful_withdrawal_sets_message_and_updates_balance(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner', balance=Decimal('50.00'))

        response = self.client.post(reverse('banking:withdraw_submit', args=[account.pk]), {'amount': '10.00'}, follow=True)

        account.refresh_from_db()
        self.assertEqual(account.balance, Decimal('40.00'))
        self.assertContains(response, 'Withdrawal completed successfully.')

    def test_overdraft_renders_inline_error(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner', balance=Decimal('50.00'))

        response = self.client.post(reverse('banking:withdraw_submit', args=[account.pk]), {'amount': '55.00'})

        account.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(account.balance, Decimal('50.00'))
        self.assertContains(response, 'Withdrawal rejected because the amount exceeds the available balance.')

    def test_transaction_history_page_renders(self):
        account = BankAccount.objects.create(account_holder_name='Workshop Learner')
        account.deposit('10.00')

        response = self.client.get(reverse('banking:transaction_list', args=[account.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DEPOSIT')