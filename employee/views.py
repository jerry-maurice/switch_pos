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
from product.models import Product
from sale.models import Order, OrderDetail

# Create your views here.
@login_required
def employee_verification(request):
    '''
    verify employee before display pos 
    '''
    user = request.user
    if request.method == 'GET':
        today = date.today()
        employee = get_object_or_404(Employee, user=user)
        company = employee.company
        if Employee_Register.objects.filter(Q(employee=employee) & Q(access_from__lte=today) & Q(access_to__gte=today)).exists():
            products = Product.objects.all().filter(company=company,available=True)
            order = None
            products_in_cart = None
            total = 0
            if Order.objects.filter(is_in_cart=True, company=company).exists():
                order = get_object_or_404(Order, is_in_cart=True)
                products_in_cart = OrderDetail.objects.filter(order=order)
                for item in products_in_cart:
                    total = total + item.quantity
            context = {
                'company':company,
                'employee':employee,
                'products':products,
                'order':order,
                'products_in_cart':round(total),
            }
            return render(request, 'sale/shop_product.html',context)
        else:
            context= {
                'message':'Please contact manager. You are not scheduled to work today'
            }
            return render(request, 'authentication/login.html',context)

