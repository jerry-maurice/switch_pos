from django.db import models
from company.models import Company, Company_location

# Create your models here.
class Category(models.Model):
    '''
    inventory category
    '''
    name = models.CharField(null=False, max_length=250)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    '''
    inventory
    '''
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    productNumber = models.CharField(null=True, blank=True, unique=True, db_index=True, max_length=255)
    name = models.CharField(null=False, max_length=250)
    image = models.FileField()
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False, default=0)
    available = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company")
    location = models.ForeignKey(Company_location, on_delete=models.CASCADE, related_name="location")

    def __str__(self):
        return self.name


