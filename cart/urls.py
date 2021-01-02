from django.urls import path
from cart import views


urlpatterns = [
    path('select/<int:product_id>', views.product_select, name='item-select' ),
    path('add/<int:product_id>', views.cart_add, name='add-cart' ),
    path('detail/', views.cart_detail, name='detail-cart' ),
    path('<int:detail_id>/delete', views.cart_remove, name="delete-cart"),
    path('order/<int:order_id>/payment', views.payment_view, name="payment")
]