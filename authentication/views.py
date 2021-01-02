from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from account.models import Account
from administration.models import Staff
from employee.models import Employee
from administration.views import dashboard
from account.views import account_dashboard
from employee.views import employee_verification
# from account.models import Account

# Create your views here.
def authentication(request):
    '''
    login verification
    '''
    if request.method == 'GET':
        return render(request, 'authentication/login.html')
    if request.method == 'POST':
        username = request.POST['login-username']
        password = request.POST['login-password']
        # authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if Staff.objects.filter(user=user).exists():
                return redirect(dashboard)
            elif Account.objects.filter(user=user).exists():
                return redirect(account_dashboard)
            elif Employee.objects.filter(user=user).exists():
                return redirect(employee_verification)
            else:
                context={
                    'message':'Please, contact support. Your account registration is incomplete'
                }
                return render(request, 'authentication/login.html',context)
        else:
            context = {
                'message':'Please try again. User not found'
            }
            return render(request, 'authentication/login.html',context)


def loging_out(request):
    '''
    loging a user out
    '''
    logout(request)
    return redirect(authentication)