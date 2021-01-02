from django.db import models
from phone_field import PhoneField
from account.models import Account

# Create your models here.
class Company(models.Model):
    '''
    owner business
    '''
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_company")
    name = models.CharField(null=False, max_length=250)
    about = models.TextField(blank=True, null=False)
    phone = PhoneField(blank=False, help_text="Please enter phone number")

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class Company_location(models.Model):
    '''
    different location of company
    '''
    phone = PhoneField(blank=False, help_text="Please enter phone number")
    address = models.CharField(blank=False, null=False, max_length=255)
    city = models.CharField(null=False, blank=True, max_length=255)
    state = models.CharField(null=False, blank=True, max_length=255)
    country = models.CharField(null=False, max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_location")

    def __str__(self):
        return ("Phone %s, company %s" % (self.phone, self.company.name))