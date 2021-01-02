from django.contrib import admin
from product.models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','image', 'price','quantity','available','created','updated','category','company','location']
    list_filter = ['name', 'available']
    list_editable = ['price','available']