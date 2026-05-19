from decimal import Decimal
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models, transaction


class BankAccount(models.Model):
	account_holder_name = models.CharField(max_length=255)
	account_number = models.CharField(max_length=32, unique=True, blank=True)
	balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['account_holder_name', 'id']

	def __str__(self):
		return f'{self.account_holder_name} ({self.account_number})'

	def save(self, *args, **kwargs):
		if not self.account_number:
			self.account_number = self.generate_account_number()
		super().save(*args, **kwargs)

	def generate_account_number(self):
		while True:
			candidate = f'ACC-{uuid4().hex[:8].upper()}'
			if not BankAccount.objects.filter(account_number=candidate).exists():
				return candidate

	def deposit(self, amount):
		normalized_amount = self._normalize_amount(amount)
		with transaction.atomic():
			account = BankAccount.objects.select_for_update().get(pk=self.pk)
			account.balance += normalized_amount
			account.save(update_fields=['balance'])
			self.balance = account.balance
			return Transaction.objects.create(
				bank_account=account,
				transaction_type=Transaction.TransactionType.DEPOSIT,
				amount=normalized_amount,
			)

	def withdraw(self, amount):
		normalized_amount = self._normalize_amount(amount)
		with transaction.atomic():
			account = BankAccount.objects.select_for_update().get(pk=self.pk)
			if normalized_amount > account.balance:
				raise ValidationError('Withdrawal rejected because the amount exceeds the available balance.')
			account.balance -= normalized_amount
			account.save(update_fields=['balance'])
			self.balance = account.balance
			return Transaction.objects.create(
				bank_account=account,
				transaction_type=Transaction.TransactionType.WITHDRAWAL,
				amount=normalized_amount,
			)

	@staticmethod
	def _normalize_amount(amount):
		decimal_amount = Decimal(str(amount))
		if decimal_amount <= Decimal('0.00'):
			raise ValidationError('Enter an amount greater than 0.')
		return decimal_amount.quantize(Decimal('0.01'))


class Transaction(models.Model):
	class TransactionType(models.TextChoices):
		DEPOSIT = 'DEPOSIT', 'Deposit'
		WITHDRAWAL = 'WITHDRAWAL', 'Withdrawal'

	bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
	transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at', '-id']

	def __str__(self):
		return f'{self.transaction_type} {self.amount}'
