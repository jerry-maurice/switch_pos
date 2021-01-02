from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import  User
from django.views import generic

import logging
from datetime import date, datetime
from django.utils import timezone

from administration.models import Plan, Status
from account.models import Account, Account_Plan
from company.models import Company, Company_location
from administration.utils import get_current_users

from django.contrib.sessions.models import Session

# get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
@staff_member_required
def dashboard(request):
    '''
    admin dashboard
    '''
    user = request.user
    if request.method == 'GET':
        accounts = Account.objects.all()
        companies = Company.objects.all()
        logged_user = get_current_users()
        context = {
                'accounts':accounts,
                'companies':companies,
                'user':user,
                'current_users':logged_user,
        }
        return render(request, 'administration/dashboard.html',context)


@staff_member_required
def account_creation(request):
    if request.method == 'GET':
        plans = Plan.objects.all().order_by('price')
        context = {
                'plans':plans
        }
        return render(request, 'administration/create_account.html', context)
    if request.method == 'POST':
        logger.info('creating a new account')
        # authentication info
        username = request.POST['username']
        password = request.POST['password']
        # user info
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        # picture = request.POST['picture']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        # business info
        name = request.POST['name']
        about = request.POST['about']
        '''company_phone = request.POST['company_phone']
        company_address = request.POST['company_address']
        company_city = request.POST['company_city']
        company_state = request.POST['company_state']
        company_country = request.POST['company_country']'''
        # Plan info
        plan_id = request.POST['plan']
        trial = request.POST['trial']
        
        # saving user info
        user = User.objects.create_user(username, email, password)
        user.last_name = lastName
        user.first_name = firstName
        user.save()
        # saving account
        status = get_object_or_404(Status,name='PENDING')
        account = Account(user=user, phone=phone, address=address, city=city, state=state, country=country, status=status)
        account.save()
        # saving business
        company = Company(name=name, about=about, account=account)
        company.save()
        # saving plan
        plan = get_object_or_404(Plan, pk=plan_id)
        if trial is not None:
                account_plan = Account_Plan(plan=plan, account=account, trial=True)
                account.status = get_object_or_404(Status,name='ACTIVE')
                account.save()
                account_plan.save()
        else:
                account_plan = Account_Plan(plan=plan, account=account)
                account_plan.save()
        return redirect(dashboard)


@staff_member_required
def account_view(request):
    '''
    show a list of account
    '''
    if request.method == 'GET':
        accounts = Account.objects.all()
        context = {
                'accounts':accounts
        }
        return render(request, 'administration/view_account.html',context)


@staff_member_required
def account_view_detail(request, account_id):
        '''
        detail view of each account
        '''
        account = get_object_or_404(Account, pk=account_id)
        company = get_object_or_404(Company, account=account)
        account_plan = get_object_or_404(Account_Plan, account=account, is_active=True)
        if request.method == 'GET':
                plans = Plan.objects.all().order_by('price')
                status = Status.objects.all()
                context = {
                        'account':account,
                        'plans':plans,
                        'account_plan':account_plan,
                        'status':status,
                        'company':company,
                }
                return render(request, 'administration/view_account_detail.html', context)
        if request.method == 'POST':
                user = account.user
                logger.info('Modify account')
                # user info
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                # picture = request.POST['picture']
                user.email = request.POST['email']
                account.phone = request.POST['phone']
                account.address = request.POST['address']
                account.city = request.POST['city']
                account.state = request.POST['state']
                account.country = request.POST['country']
                # business info
                company.name = request.POST['name']
                company.about = request.POST['about']
                '''company.phone = request.POST['company_phone']
                company.address = request.POST['company_address']
                company.city = request.POST['company_city']
                company.state = request.POST['company_state']
                company.country = request.POST['company_country']'''
                # Plan info - update old plan and add new plan
                plan_id = request.POST['plan']
                plan = get_object_or_404(Plan, pk=plan_id)
                if plan != account_plan.plan:
                        account_plan.is_active = False
                        account_plan.save()
                        new_account_plan = Account_Plan(plan=plan, account=account, trial=False)
                        new_account_plan.save()
                # status
                account.status = get_object_or_404(Status,pk=request.POST['status'])
                # saving user, company
                user.save()
                account.save()
                company.save()
                return redirect(account_view)


class CompanyView(generic.ListView):
        template_name = 'administration/view_company.html'
        queryset = Company.objects.all()
        context_object_name = 'company_list'


def CompanyLocationView(request, company_id):
        company = get_object_or_404(Company, pk=company_id)
        if request.method == 'GET':
                locations = Company_location.objects.all().filter(company=company)
                context={
                        'locations':locations,
                        'company':company,
                }
                return render(request, 'administration/view_company_location.html', context)


