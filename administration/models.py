from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField


# Create your models here.
class Status(models.Model):
    '''
    list of choices for status
    '''
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"


class Staff(models.Model):
    '''
    info about someone working at switch
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.URLField(blank=True, null=True)
    phone = PhoneField(blank=False, help_text='Please enter phone number')
    address = models.CharField(blank=True, null=True, max_length=255)
    city = models.CharField(blank=True, null=True, max_length=255)
    state = models.CharField(blank=True, null=True, max_length=255)
    country = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.user.first_name +' '+self.user.last_name


class Plan(models.Model):
    '''
    List of all  plan and their description
    '''
    name = models.CharField(null=False, max_length=500)
    description = models.TextField(null=False)
    employee = models.PositiveIntegerField(null=False)
    price = models.FloatField(null=False)

    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    
