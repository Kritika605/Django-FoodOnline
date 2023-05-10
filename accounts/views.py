from django.shortcuts import render,redirect
from django.views import View
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from django.contrib import messages,auth
from .utils import detectUser,send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

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
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit= False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()

            # Send verification email
            mail_subject = "Please activate your account"
            email_template = "accounts/emails/account_verification_email.html"
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request , " Your account has been registered successfully!")
            return redirect('registeruser')
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
            return redirect("vendorDashboard")
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

                # Send verification email
                mail_subject = "Please activate your account"
                email_template = "accounts/emails/account_verification_email.html"
                send_verification_email(request,user,mail_subject,email_template)
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
    
def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations ! Your account is activate")
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')

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

class Forgot_password(View):
    def get(self,request):
        return render(request,'accounts/forgot_password.html')
    
    def post(self,request):
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = "Reset your password"
            email_template = "accounts/emails/reset_password_email.html"
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,"Password reset link has been sent to your email address")
            return redirect('login')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgot_password')

def reset_password_validate(request,uidb64,token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request, "Please reset your password.")
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired.')
        return redirect('myAccount')

class Reset_password(View):
    def get(self,request):
        return render(request,'accounts/reset_password.html')
    
    def post(self,request):
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request,"Password reset successfull.")
            return redirect('login')
        else:
            messages.error(request,'Password does not match.')
            return redirect('reset_password')
