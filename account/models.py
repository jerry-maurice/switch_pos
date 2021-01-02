from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from datetime import timedelta, date
from administration.models import Plan, Status

# Create your models here.
class Account(models.Model):
    '''
    The owner of the business
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.URLField(blank=True, null=True)
    phone = PhoneField(blank=False, help_text='Please enter phone number')
    address = models.CharField(blank=False, null=False, max_length=255)
    city = models.CharField(null=False, blank=True, max_length=255)
    state = models.CharField(null=False, blank=True, max_length=255)
    country = models.CharField(null=False, max_length=255)
    status = models.ForeignKey(Status, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name +' '+self.user.last_name


class Account_Plan(models.Model):
    '''
    Chosen plan
    '''
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='account_plan')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_holder')
    started = models.DateTimeField(auto_now_add=True)
    trial = models.BooleanField(default=False)
    last_paid = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    @property
    def renew_date(self):
        if self.last_paid is not None and self.last_paid == self.started:
            return self.last_paid +  timedelta(days=30)
        return self.started +  timedelta(days=15)
        
    def __str__(self):
        return self.plan.name +' - '+ self.account.user.email


class Account_transaction(models.Model):
    '''
    list of bills and payments
    '''
    bill_created = models.DateField(auto_now_add=True)
    bill_due = models.DateField(null=False)
    bill_modified = models.DateField(auto_now=True)
    amount_due = models.FloatField(null=False)
    amount_received = models.FloatField(null=False, default=0.00)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_transaction_holder')
    account_plan = models.ForeignKey(Account_Plan, on_delete=models.CASCADE, related_name='account_transaction_plan')

    class Meta:
        ordering = ('-bill_created',)
        
    def __str__(self):
        return "{}".format(self.bill_due)