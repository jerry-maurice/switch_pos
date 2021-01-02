from django.urls import path
from administration import views


urlpatterns = [
    path('account/add/', views.account_creation, name='add-account' ),
    path('accounts/view/', views.account_view, name='view-account' ),
    path('account/<int:account_id>/view/', views.account_view_detail, name='view-account-detail' ),
    path('company/view/', views.CompanyView.as_view(), name='view-company' ),
    path('company/<int:company_id>/location', views.CompanyLocationView, name='location-company' ),
    path('dashboard/', views.dashboard, name='admin-dashboard' ),
]