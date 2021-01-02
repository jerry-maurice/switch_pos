from django.contrib import admin
from employee.models import Employee, Employee_Register

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user','phone','company','is_active')


admin.site.register(Employee_Register)