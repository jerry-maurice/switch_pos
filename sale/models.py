from django.db import models
from django.contrib.auth.models import User
from register.models import Register
from product.models import Product
from employee.models import Employee
from company.models import Company

# Create your models here.
class Order(models.Model):
    placement = models.DateTimeField(auto_now_add=True)
    fulfillment = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE,  related_name='employee_order')
    is_in_cart = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=False)
    comment = models.TextField()
    company = models.ForeignKey(Company, on_delete = models.CASCADE)

    class Meta:
        ordering = ('-placement',)

    def __str__(self):
        return f'{self.employee.user.first_name}. {self.comment}'


class OrderDetail(models.Model):
    '''
    detail about order
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    quantity = models.FloatField(null=False)
    #fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name='order_fee', blank=True, null=True)
    #coupon = models.ForeignKey(Coupon, on_delete = models.CASCADE, related_name='order_coupon', blank=True, null=True)
    order = models.ForeignKey(Order, on_delete= models.CASCADE, related_name='order_detail', null=True)

    @property
    def total_price(self):
        return round(self.product.price * self.quantity,2)

    def __str__(self):
        return f'{self.product.price}. {self.quantity}'


class Payment(models.Model):
    '''
    record of payment made  by customer
    '''
    method = models.CharField(null=False, max_length=250)
    is_valid = models.BooleanField(default=True)
    amount_due = models.FloatField(null=False)
    amount_paid = models.FloatField(null=False, default=0.0)
    amount_returned = models.FloatField(null=True, default=0.0)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name='payment_order')
    comment = models.TextField()


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.amount_due}'