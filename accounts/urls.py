from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('registeruser/', views.RegisterUser.as_view(), name='registeruser'),
    path('registervendor/', views.RegisterVendor.as_view(), name='registervendor'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
]