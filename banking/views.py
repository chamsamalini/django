from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BankAccountCreateForm, DepositForm, WithdrawForm
from .models import BankAccount


def home_view(request):
	return render(request, 'banking/home.html')


def account_create_view(request):
	form = BankAccountCreateForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		account = form.save()
		return redirect('banking:account_detail', pk=account.pk)
	return render(request, 'banking/account_create.html', {'form': form})


def account_detail_view(request, pk):
	account = get_object_or_404(BankAccount, pk=pk)
	return render(request, 'banking/account_detail.html', {'account': account})


def deposit_view(request, pk):
	account = get_object_or_404(BankAccount, pk=pk)
	form = DepositForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		account.deposit(form.cleaned_data['amount'])
		messages.success(request, 'Deposit completed successfully.')
		return redirect('banking:account_detail', pk=account.pk)
	return render(request, 'banking/deposit.html', {'account': account, 'form': form})


def withdraw_view(request, pk):
	account = get_object_or_404(BankAccount, pk=pk)
	form = WithdrawForm(account, request.POST or None)
	if request.method == 'POST' and form.is_valid():
		account.withdraw(form.cleaned_data['amount'])
		messages.success(request, 'Withdrawal completed successfully.')
		return redirect('banking:account_detail', pk=account.pk)
	return render(request, 'banking/withdraw.html', {'account': account, 'form': form})


def transaction_list_view(request, pk):
	account = get_object_or_404(BankAccount, pk=pk)
	return render(
		request,
		'banking/transaction_list.html',
		{'account': account, 'transactions': account.transactions.all()},
	)
