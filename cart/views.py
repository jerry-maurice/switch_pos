from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account.decorators import account_user_required
from django.contrib.auth.models import  User
from django.db.models import Q
from django.views.decorators.http import require_POST,require_GET
from cart.forms import CartAddProductForm

import logging
from datetime import date, datetime
from django.utils import timezone

from product.models import Product
from sale.models import Order, OrderDetail, Payment
from employee.models import Employee_Register
from employee.views import employee_verification, Employee

# Create your views here.
@login_required
@require_GET
def product_select(request, product_id):
    employee = get_object_or_404(Employee, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    products_in_cart = None
    total = 0
    if Order.objects.filter(is_in_cart=True, employee=employee).exists():
        order = get_object_or_404(Order, is_in_cart=True)
        products_in_cart = OrderDetail.objects.filter(order=order)
        for item in products_in_cart:
            total = total + item.quantity
    context = {
        'product':product,
        'products_in_cart':round(total),
    }
    return render(request, 'sale/quantity.html', context)


@login_required
@require_POST
def cart_add(request, product_id):
    employee = get_object_or_404(Employee, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    old_quantity = product.quantity
    quantity = request.POST['quantity']
    if int(quantity) > old_quantity:
        return redirect(employee_verification)
    else:
        if Order.objects.filter(is_in_cart=True).exists():
            cart = get_object_or_404(Order, is_in_cart=True)
        else:
            cart = Order(employee=employee)
            cart.save()
        order_detail = OrderDetail(product=product, quantity=quantity, order=cart)
        order_detail.save()
        product.quantity = old_quantity - int(quantity)
        if int(quantity) == old_quantity:
            product.available = False
        product.save()
    return redirect(employee_verification)


@login_required
@require_GET
def cart_remove(request, detail_id):
    order_detail = get_object_or_404(OrderDetail, pk=detail_id)
    product = order_detail.product
    quantity = order_detail.quantity
    if product.quantity == 0:
        product.available = True
    product.quantity = product.quantity+quantity
    product.save()
    order_detail.delete()
    return redirect(cart_detail)


@login_required
@require_GET
def cart_detail(request):  
    order = None
    products_in_cart = None
    if Order.objects.filter(is_in_cart=True).exists():
        order = get_object_or_404(Order, is_in_cart=True)
        products_in_cart = OrderDetail.objects.filter(order=order)
        total = 0
        for item in products_in_cart:
            total = total + item.quantity
        totalPrice = 0.0
        for i in range(len(products_in_cart)):
            totalPrice = totalPrice+ (products_in_cart[i].quantity * products_in_cart[i].product.price)
    context = {
        'order':order,
        'products_in_cart':round(total),
        'order_in_cart':products_in_cart,
        'total_price':round(totalPrice,2),
    }
    return render(request, 'cart/detail.html', context)


@login_required
def payment_view(request, order_id):
    today = date.today()
    order = get_object_or_404(Order, pk=order_id)
    employee = order.employee
    employee_register = Employee_Register.objects.filter(Q(employee=employee) & Q(access_from__lte=today) & Q(access_to__gte=today)).first()
    register = employee_register.register
    detail = OrderDetail.objects.filter(order=order)
    totalPrice = 0.0
    for i in range(len(detail)):
        totalPrice = totalPrice+ (detail[i].quantity * detail[i].product.price)
    if request.method == 'GET':
        context = {
            'order':order,
            'amount_due':round(totalPrice,2),
        }
        return render(request, 'sale/payment.html',context)
    if request.method == 'POST':
        method = request.POST['method_payment']
        paid = request.POST['amount_paid']
        returned = float(paid) - totalPrice
        if returned < 0:
            valid = False
        else:
            valid = True
        if register.balance < returned:
            context = {
                'message':'Cash register \' balance is low. Order has been cancelled. Please add  more fund to this cash register'
            }
            return render(request, 'register/message.html',context)
        else:
            payment = Payment(method=method,is_valid=valid, amount_due=round(totalPrice,2), amount_paid=float(paid), amount_returned=round(float(returned),2), order=order)
            payment.save()
            register.balance = round((totalPrice - returned),2)
            register.save()
            order.is_in_cart = False
            order.is_valid = True
            order.save()
            context = {
                'order':order,
                'order_in_cart':detail,
                'payment':payment
            }
            return render(request,'sale/invoice.html',context)

            