from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.myAccount),
    path('registeruser/', views.RegisterUser.as_view(), name='registeruser'),
    path('registervendor/', views.RegisterVendor.as_view(), name='registervendor'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),  

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),    
    path('forgot_password/', views.Forgot_password.as_view(), name='forgot_password'),   
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),   
    path('reset_password/', views.Reset_password.as_view(), name='reset_password'),   
    path('vendor/', include('vendor.urls')),   

]