from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account.decorators import account_user_required
from django.contrib.auth.models import  User

import logging
from datetime import date, datetime
from django.utils import timezone

from employee.models import Employee, Register_Log
from company.models import Company, Company_location
from account.models import Account, Account_Plan
from product.models import Product
from register.models import Register
from fund.models import Fund, Transaction

# get an instance of a logger
logger = logging.getLogger(__name__)

@login_required
@account_user_required
def add_register(request):
    if request.method == 'GET':
        account = get_object_or_404(Account, user=request.user)
        company = get_object_or_404(Company, account=account)
        registers = Register.objects.filter(company=company, is_active=True)
        locations = Company_location.objects.filter(company=company)
        context={
            'registers':registers,
            'company':company,
            'locations':locations,
        }
        return render(request, 'register/registers.html', context)
    if request.method == 'POST':
        location = get_object_or_404(Company_location, pk=request.POST['location'])
        register = Register(identification=request.POST['identification'], min_balance=request.POST['min_balance'], max_balance=request.POST['max_balance'],location=location, company=location.company)
        register.save()
        return redirect(add_register)


@login_required
@account_user_required
def remove_register(request, register_id):
    '''
    remove register
    '''
    if request.method == 'GET':
        register = get_object_or_404(Register, pk=register_id)
        if register.balance == 0:
            register.delete()
        return redirect(add_register)


@login_required
@account_user_required
def operation_register(request, register_id):
    '''
    add or remove money in register
    
    '''
    account = get_object_or_404(Account, user=request.user)
    company = get_object_or_404(Company, account=account)
    register = get_object_or_404(Register, pk=register_id)
    fund  = get_object_or_404(Fund, company=company)
    if request.method == 'GET':
        context ={
            'company':company,
            'register':register,
            'fund':fund,
        }
        return render(request, 'register/operation.html',context)
    if request.method == 'POST':
        operationType = request.POST['type']
        amount = request.POST['amount']
        previous_amount = fund.funds
        register_previous_amount = register.balance
        source = ""
        actual_balance = 0
        source = "Register"
        if operationType == '1':
            actual_balance = float(previous_amount) - float(amount)
            register_balance =  float(register_previous_amount) + float(amount)
            logger.info(actual_balance)
            if  actual_balance < 0:
                context = {
                    'message':'Low in fund. Transaction can\'t be completed'
                }
                return render(request, 'register/message.html',context)
            else:
                fund.funds = actual_balance
                fund.save()
                transaction = Transaction(withdrew=amount, previous_balance=previous_amount, 
                            actual_balance=round(actual_balance,2), source=source, fund=fund)
                transaction.save()
                register.balance  = register_balance
                register.save()
                log = Register_Log(actual_balance=register_balance, deposited=amount,  previous_balance=register_previous_amount, register=register)
                log.save()
        elif operationType == '0':
            actual_balance = float(previous_amount) + float(amount)
            register_balance =  float(register.balance) - float(amount)
            fund.funds = actual_balance
            fund.save()
            transaction = Transaction(deposited=amount, previous_balance=previous_amount, 
                        actual_balance=round(actual_balance,2), source=source, fund=fund)
            transaction.save()
            register.balance  = register_balance
            register.save()
            log = Register_Log(actual_balance=register_balance, withdrew=amount,  previous_balance=register_previous_amount, register=register)
            log.save()
        return redirect(add_register)




