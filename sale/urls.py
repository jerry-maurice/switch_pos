from django.urls import path
from sale import views


urlpatterns = [
    path('order/submit/', views.order_submission, name='order-submission' ),
]