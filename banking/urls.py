from django.urls import path

from . import views

app_name = 'banking'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/create/', views.account_create_view, name='account_create'),
    path('accounts/create/submit/', views.account_create_submit_view, name='account_create_submit'),
    path('accounts/<int:pk>/', views.account_detail_view, name='account_detail'),
    path('accounts/<int:pk>/deposit/', views.deposit_view, name='deposit'),
    path('accounts/<int:pk>/deposit/submit/', views.deposit_submit_view, name='deposit_submit'),
    path('accounts/<int:pk>/withdraw/', views.withdraw_view, name='withdraw'),
    path('accounts/<int:pk>/withdraw/submit/', views.withdraw_submit_view, name='withdraw_submit'),
    path('accounts/<int:pk>/transactions/', views.transaction_list_view, name='transaction_list'),
]