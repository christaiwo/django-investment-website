from os import name
from re import template
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('test', views.test, name="test"),
    path('', views.home, name="home"),



     # for user area 
    path('account/register', views.account_register, name="account_register"),
    path('account/login', views.account_login, name="account_login"),
    path('account/logout', views.account_logout, name="account_logout"),
    path('account/', views.account, name="account"),
    path('account/deposit', views.account_deposit, name="account_deposit"),
    path('account/deposit/<str:pk>', views.account_deposit_check, name="account_deposit_check"),
    path('account/withdraw', views.account_withdraw, name="account_withdraw"),
    path('account/pricing', views.account_pricing, name="account_pricing"),
    path('account/audit/<str:pk>', views.account_audit, name="account_audit"),
    path('account/investments', views.account_investment, name="account_investment"),
    path('account/bank', views.account_bank, name="account_bank"),
    path('account/profile', views.account_profile, name="account_profile"),





]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


# handler404 = "base.views.page_not_found_view"
# handler500 = "base.views.internal_server_error_found_view"