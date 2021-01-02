from django.urls import path
from fund import views


urlpatterns = [
    path('overview/', views.overview, name='overview' ),
    path('deposit/', views.deposit, name='fund-deposit' ),
]