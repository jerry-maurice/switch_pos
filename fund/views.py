from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account.decorators import account_user_required
from django.contrib.auth.models import  User

import logging
from datetime import date, datetime
from django.utils import timezone

from fund.models import Fund, Transaction
from account.models import Account
from company.models import Company

# get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
@login_required
@account_user_required
def overview(request):
    if request.method == 'GET':
        account = get_object_or_404(Account, user=request.user)
        company = get_object_or_404(Company, account=account)
        if Fund.objects.filter(company=company).exists():
            fund = get_object_or_404(Fund,company=company)
        else:
            fund = Fund(company=company)
            fund.save()
            
        transactions = Transaction.objects.filter(fund=fund)
        context = {
            'fund':fund,
            'company':company,
            'transactions':transactions,
        }
        return render(request,'fund/overview.html',context)


@login_required
@account_user_required
def deposit(request):
    account = get_object_or_404(Account, user=request.user)
    company = get_object_or_404(Company, account=account)
    fund = get_object_or_404(Fund,company=company)
    if request.method == 'GET':
        context = {
            'fund':fund,
            'company':company,
        }
        return render(request, 'fund/deposit.html', context)
    if request.method == 'POST':
        deposit_amount = request.POST['amount']
        source = request.POST['source']
        comment = request.POST['comment']
        previous_amount = fund.funds
        actual_balance = float(previous_amount) + float(deposit_amount)
        fund.funds = actual_balance
        fund.save()
        transaction = Transaction(deposited=deposit_amount, previous_balance=previous_amount, 
                    actual_balance=actual_balance, source=source, fund=fund, comment=comment)
        transaction.save()
        return redirect(overview)
