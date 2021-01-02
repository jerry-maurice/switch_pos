from django.contrib import admin
from administration.models import Status, Staff, Plan

# Register your models here.
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user','picture','phone','address','city','state','country')
    list_filter = ('phone', 'country')


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name','description','employee','price')