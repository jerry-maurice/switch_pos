from django.contrib import admin
from company.models import Company, Company_location

# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','about','account' )


@admin.register(Company_location)
class CompanyLocationAdmin(admin.ModelAdmin):
    list_display = ('phone','address','city','state','country','company' )