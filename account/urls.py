from django.urls import path
from account import views


urlpatterns = [
    path('dashboard/', views.account_dashboard, name='account-dashboard' ),
    path('employee/add', views.add_employee, name='add-employee' ),
    path('employees/view', views.view_employees, name='view-employee' ),
    path('employee/<int:employee_id>/view', views.employee_detail, name='view-employee-detail' ),
    path('register/assigned', views.assign_register, name='assign-register' ),
    path('register/assigned/<int:assign_id>/delete', views.remove_assigned_register, name='assign-remove' ),
]