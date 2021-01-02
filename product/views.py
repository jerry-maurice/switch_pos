from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account.decorators import account_user_required
from django.contrib.auth.models import  User

import logging
from datetime import date, datetime
from django.utils import timezone

from product.models import Product, Category
from account.models import Account
from company.models import Company, Company_location

# get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
@login_required
@account_user_required
def view_inventory(request):
    '''
    list of all the product
    '''
    if request.method == 'GET':
        account = get_object_or_404(Account, user=request.user)
        company = get_object_or_404(Company, account=account)
        products = Product.objects.all().filter(company=company)
        context = {
            'company':company,
            'products':products,
        }
        return render(request, 'product/inventory.html',context)


@login_required
@account_user_required
def add_product(request):
    '''
    adding new products
    '''
    account = get_object_or_404(Account, user=request.user)
    company = get_object_or_404(Company, account=account)
    if request.method == 'GET':
        categories = Category.objects.all()
        locations = Company_location.objects.all().filter(company=company)
        context = {
            'categories':categories,
            'locations':locations,
        }
        return render(request, 'product/add_product.html',context)
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=request.POST['category'])
        upc = request.POST['product_number']
        name = request.POST['name']
        picture = request.FILES['product_image']
        price = request.POST['price']
        quantity = request.POST['quantity']
        description = request.POST['description']
        location = get_object_or_404(Company_location, pk=request.POST['location'])
        if int(quantity) > 0:
            available = True
        product = Product(category=category, productNumber=upc, name=name, image=picture, price=price, quantity=quantity, available=available,company=company, location=location, description=description)
        product.save()
        logger.info(picture.name)
        logger.info(picture.size)
        return redirect(view_inventory)


@login_required
@account_user_required
def delete_product(request, product_id):
    if request.method == 'GET':
        product = Product.objects.get(pk=product_id)
        product.delete()
        logger.info("delete product")
        return redirect(view_inventory)


@login_required
@account_user_required
def edit_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'GET':
        context={
            'product':product,
        }
        return render(request, 'product/edit_product.html', context)
    if request.method == 'POST':
        product.productNumber = request.POST['product_number']
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        if request.POST['quantity'] == '0':
            product.available = False
        elif int(request.POST['quantity']) > 0:
            product.available = True
        product.save()
        return redirect(view_inventory)

    



