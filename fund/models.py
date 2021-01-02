from django.db import models
from company.models import Company

# Create your models here.
class Fund(models.Model):
    '''
    '''
    funds = models.FloatField(null=False, default=0.00)
    currency = models.CharField(null=False, default="Haitian Gourde", max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_fund')
        
    def __str__(self):
        return f'{self.funds}. {self.country.name}'


class Transaction(models.Model):
    '''
    funding transaction
    '''
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deposited = models.FloatField(null=False, default=0.0)
    withdrew = models.FloatField(null=False, default=0.0)
    previous_balance = models.FloatField(null=False, default=0.0)
    actual_balance = models.FloatField(null=False, default=0.0)
    source = models.CharField(null=True, max_length=200)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='transaction_fund')
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return f'{self.created}. {self.previous_balance}. {self.actual_balance}'
