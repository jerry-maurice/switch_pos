from django.contrib import admin
from account.models import Account, Account_Plan

# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user','picture','phone', 'address','city','state','country')


admin.site.register(Account_Plan)