from django.urls import path,include
from . import views
from accounts import views as AccountViews
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', AccountViews.vendorDashboard,name = 'vendor'),
    path('profile/', views.vprofile,name = 'vprofile'),
    

]