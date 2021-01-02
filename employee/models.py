from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from company.models import Company
from administration.models import Status
from register.models import Register

# Create your models here.
class Employee(models.Model):
    '''
    employee
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.URLField(blank=True, null=True)
    phone = PhoneField(blank=False, help_text='Please enter phone number')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_employee")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s, %s" % (self.user.first_name, self.user.last_name)


class Employee_Register(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employee")
    register = models.ForeignKey(Register, on_delete=models.CASCADE, related_name="register")
    access_from = models.DateField(null=False)
    access_to = models.DateField()
    time_start = models.TimeField(null=False)
    time_stop = models.TimeField(null=False)

    def __str__(self):
        return "%s - %s" %(self.employee.user.first_name, self.register.identification)


class Register_Log(models.Model):
    '''
    all transactions made are recorded
    '''
    deposited = models.FloatField(null=False, default=0.0)
    withdrew = models.FloatField(null=False, default=0.0)
    previous_balance = models.FloatField(null=False, default=0.0)
    actual_balance = models.FloatField(null=False, default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    register = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='log_register')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_register', blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return f'{self.created}. {self.previous_balance}. {self.actual_balance}'