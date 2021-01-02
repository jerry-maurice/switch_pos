from django.urls import path
from register import views


urlpatterns = [
    path('add/', views.add_register, name='add-register' ),
    path('<int:register_id>/remove', views.remove_register, name='remove-register' ),
    path('<int:register_id>/operation', views.operation_register, name='operation-register' ),
]