from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account.decorators import account_user_required
from django.contrib.auth.models import  User
from django.db.models import Q

import logging
from datetime import date, datetime
from django.utils import timezone

from employee.models import Employee, Employee_Register
from company.models import Company
from account.models import Account, Account_Plan
from product.models import Product
from register.models import Register
from sale.models import Order

# get an instance of a logger
logger = logging.getLogger(__name__)

@login_required
@account_user_required
def account_dashboard(request):
    '''
    account holder dasboard
    '''
    user = request.user
    if request.method == 'GET':
        account = get_object_or_404(Account, user=request.user)
        company = get_object_or_404(Company, account=account)
        employees = Employee.objects.all().filter(company=company)
        products = Product.objects.all().filter(company=company)
        products_available = Product.objects.all().filter(company=company, available=True)
        order = Order.objects.filter(company=company)
        context = {
            'employees':employees,
            'user':user,
            'company':company,
            'products':products,
            'a_products':products_available,
            'order':order,
        }
        return render(request, 'account/dashboard.html',context)


@login_required
@account_user_required
def add_employee(request):
    '''
    creating new employee
    '''
    account = get_object_or_404(Account, user=request.user)
    company = get_object_or_404(Company, account=account)
    account_plan = get_object_or_404(Account_Plan, account=account, is_active=True)
    if request.method == 'GET':
        logger.info("new employee to be added")
        return render(request, 'account/new_employee.html')
    if request.method == 'POST':
        # verifying account plan before create a new object
        number_employee = Employee.objects.all().filter(company=company, is_active=True).count()
        if number_employee < account_plan.plan.employee:
            logger.info('adding new employee')
            username = request.POST['username']
            password = request.POST['password']
            # user info
            firstName = request.POST['first_name']
            lastName = request.POST['last_name']
            # picture = request.POST['picture']
            email = request.POST['email']
            phone = request.POST['phone']

            # saving user info
            user = User.objects.create_user(username, email, password)
            user.last_name = lastName
            user.first_name = firstName
            user.save()
            employee = Employee(user=user, phone=phone, company=company)
            employee.save()
            return redirect(add_employee)
        else:
            context = {
                'message':"You have reached the maximum number of employees. Contact support if you want to change your account plan"
            }
            return render(request, 'account/new_employee.html', context)


@login_required
@account_user_required
def employee_detail(request, employee_id):
    '''
    specific employee
    '''
    account = get_object_or_404(Account, user=request.user)
    company = get_object_or_404(Company, account=account)
    employee = get_object_or_404(Employee, pk=employee_id)
    account_plan = get_object_or_404(Account_Plan, account=account, is_active=True)
    if request.method == 'GET':
        context = {
            'employee':employee,
        }
        return render(request, 'account/employee_detail.html', context)
    if request.method == 'POST':
        # user info
        user = employee.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        # picture = request.POST['picture']
        user.email = request.POST['email']
        employee.phone = request.POST['phone']
        if request.POST['status']=="0":
            employee.is_active = False
        else:
            number_employee = Employee.objects.all().filter(company=company, is_active=True).count()
            if number_employee < account_plan.plan.employee:
                employee.is_active = True
            else:
                context = {
                    'employee':employee,
                    'message':"You have reached the maximum number of employees. Contact support if you want to change your account plan"
                }
                return render(request, 'account/employee_detail.html', context)
        # saving
        user.save()
        employee.save()
        return redirect(view_employees)



@login_required
@account_user_required
def view_employees(request):
    '''
    show a list of employees
    '''
    if request.method == 'GET':
        account = get_object_or_404(Account, user=request.user)
        company = get_object_or_404(Company, account=account)
        employees = Employee.objects.all().filter(company=company)
        context = {
            'employees':employees
        }
        return render(request, 'account/employee_list.html', context)


@login_required
@account_user_required
def assign_register(request):
    today = date.today()
    if request.method == 'GET':
        account = get_object_or_404(Account, user=request.user)
        company = get_object_or_404(Company, account=account)
        assign = Employee_Register.objects.filter(Q(access_from__lte=today) & Q(access_to__gte=today))
        context = {
            'assign':assign,
            'employees':Employee.objects.filter(company=company, is_active=True),
            'registers': Register.objects.filter(company=company, is_active=True),
        }
        return render(request, 'register/assign_register.html',context)
    if request.method == 'POST':
        employee = get_object_or_404(Employee, pk=request.POST['employee'])
        register = get_object_or_404(Register, pk=request.POST['register'])
        access_from = request.POST['access_from']
        access_to = request.POST['access_to']
        start_time = request.POST['time_start']
        end_time = request.POST['time_stop']
        if not Employee_Register.objects.filter(Q(employee=employee) & Q(access_from__lte=today) & Q(access_to__gte=today)).exists():
            employee_register = Employee_Register(employee=employee, register=register, access_from=access_from, access_to=access_to, time_start=start_time, time_stop=end_time)
            employee_register.save()
        return redirect(assign_register)


@login_required
@account_user_required
def remove_assigned_register(request, assign_id):
    if request.method == 'GET':
        employee_register = get_object_or_404(Employee_Register, pk=assign_id)
        employee_register.delete()
        return redirect(assign_register)