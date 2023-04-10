from django.urls import path
from . import views

urlpatterns = [
    path('registeruser/', views.RegisterUser.as_view(), name='registeruser'),
]