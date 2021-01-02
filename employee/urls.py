from django.urls import path
from employee import views


urlpatterns = [
    path('verify/', views.employee_verification, name='employee-verification' ),
]