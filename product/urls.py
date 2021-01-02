from django.urls import path
from product import views


urlpatterns = [
    path('list/', views.view_inventory, name='view-inventory' ),
    path('add/', views.add_product, name='add-inventory' ),
    path('<int:product_id>/delete/', views.delete_product, name='delete-inventory' ),
    path('<int:product_id>/edit/', views.edit_product, name='edit-inventory' ),
]