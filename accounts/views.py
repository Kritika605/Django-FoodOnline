from django.shortcuts import render,redirect
from django.views import View
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.
class RegisterUser(View):
    def get(self,request):
        form = UserForm()
        context = {
            'form' : form
        }
        return render(request, 'accounts/registeruser.html',context)
    
    def post(self,request):
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit= False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request , " Your account has been registered successfully!")
        context={
            'form' : form
        }
        return render(request, 'accounts/registeruser.html',context)