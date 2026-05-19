from django.contrib import messages
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BankAccountCreateForm, DepositForm, WithdrawForm
from .models import BankAccount


ACCOUNT_DETAIL_ROUTE = 'banking:account_detail'


@require_GET
def home_view(request):
	return render(request, 'banking/home.html')


@require_GET
def account_create_view(request):
	form = BankAccountCreateForm()
	return render(request, 'banking/account_create.html', {'form': form})


@require_POST
def account_create_submit_view(request):
	form = BankAccountCreateForm(request.POST)
	if form.is_valid():
		account = form.save()
		return redirect(ACCOUNT_DETAIL_ROUTE, pk=account.pk)
	return render(request, 'banking/account_create.html', {'form': form})


@require_GET
def account_detail_view(request, pk):
	account = get_object_or_404(BankAccount, pk=pk)
	return render(request, 'banking/account_detail.html', {'account': account})


@require_GET
def deposit_view(request, pk):
	account = get_object_or_404(BankAccount, pk=pk)
	form = DepositForm()
	return render(request, 'banking/deposit.html', {'account': account, 'form': form})


@require_POST
def deposit_submit_view(request, pk):
	account = get_object_or_404(BankAccount, pk=pk)
	form = DepositForm(request.POST)
	if form.is_valid():
		account.deposit(form.cleaned_data['amount'])
		messages.success(request, 'Deposit completed successfully.')
		return redirect(ACCOUNT_DETAIL_ROUTE, pk=account.pk)
	return render(request, 'banking/deposit.html', {'account': account, 'form': form})


@require_GET
def withdraw_view(request, pk):
	account = get_object_or_404(BankAccount, pk=pk)
	form = WithdrawForm(account)
	return render(request, 'banking/withdraw.html', {'account': account, 'form': form})


@require_POST
def withdraw_submit_view(request, pk):
	account = get_object_or_404(BankAccount, pk=pk)
	form = WithdrawForm(account, request.POST)
	if form.is_valid():
		account.withdraw(form.cleaned_data['amount'])
		messages.success(request, 'Withdrawal completed successfully.')
		return redirect(ACCOUNT_DETAIL_ROUTE, pk=account.pk)
	return render(request, 'banking/withdraw.html', {'account': account, 'form': form})


@require_GET
def transaction_list_view(request, pk):
	account = get_object_or_404(BankAccount, pk=pk)
	return render(
		request,
		'banking/transaction_list.html',
		{'account': account, 'transactions': account.transactions.all()},
	)
