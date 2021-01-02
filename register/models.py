from django.db import models
from company.models import Company, Company_location

# Create your models here.

class Register(models.Model):
    '''
    cash register
    '''
    identification = models.CharField(null=False, max_length=500)
    balance = models.FloatField(null=False, default=0)
    min_balance = models.FloatField(null=False)
    max_balance = models.FloatField(null=False)
    location = models.ForeignKey(Company_location, on_delete=models.CASCADE, related_name='location_register')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_register')
    created = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('identification',)
        
    def __str__(self):
        return f'{self.identification}. {self.balance}'


