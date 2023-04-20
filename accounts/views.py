from django.shortcuts import render,redirect
from django.views import View
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from django.contrib import messages,auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

# Create your views here.
#Restrict vendor from accessing customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
#Restrict customer from accessing vendor page.
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    
class RegisterUser(View):
    def get(self,request):
        form = UserForm()
        context = {
            'form' : form
        }
        return render(request, 'accounts/registeruser.html',context)
    
    def post(self,request):
        if request.user.is_authenticated:
            messages.warning(request, " You are already logged in")
            return redirect("dashboard")
        else:
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
    
class RegisterVendor(View):
    def get(self,request):
        form = UserForm()
        v_form = VendorForm()
        context = {
            'form': form,
            'v_form' : v_form
        }
        return render(request,'accounts/registervendor.html',context)
    
    def post(self,request):
        if request.user.is_authenticated:
            messages.warning(request, " You are already logged in")
            return redirect("dashboard")
        else:
            form = UserForm(request.POST)
            v_form = VendorForm(request.POST,request.FILES)
            if form.is_valid() and v_form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                password = form.cleaned_data['password']
                user = User.objects.create_user(first_name=first_name, last_name= last_name, username= username, email= email, password= password)
                user.role = User.VENDOR
                user.save()
                vendor = v_form.save(commit=False)
                vendor.user = user
                user_profile = UserProfile.objects.get(user= user)
                vendor.user_profile = user_profile
                vendor.save()
                messages.success(request,"Your account has been created successfully! Please wait for the approval")
            else:
                print(form.errors)
                print("invalid form")
            context = {
                'form': form,
                'v_form' : v_form
            }
            return render(request,'accounts/registervendor.html',context)
    
class Login(View):
    def get(self,request):
        if self.request.user.is_authenticated:
            messages.warning(request, " You are already logged in!")
            return redirect("myAccount")
        else:
            return render(request,'accounts/login.html')
    
    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email = email, password = password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("myAccount")
        else:
            messages.error(request,"Invalid login credential")
            return redirect("login")

class Logout(View):
    def get(self,request):
        auth.logout(request)
        messages.info(request, "You are logged out.")
        return redirect("login")

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
     return render(request, "accounts/vendorDashboard.html")