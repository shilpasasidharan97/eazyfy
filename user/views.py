import json
from django.shortcuts import render, redirect
import pyotp
from user.mixin import *
from official.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from .helpers import send_forget_password_mail
from django.contrib.auth import logout
from eazyfy.decorators import auth_customer


# CUSTOMER LOGIN
def customerlogin(request):
    if request.method == 'POST':
        number = request.POST['number']
        password = request.POST['password']
        user = authenticate(request,phone_number=number, password=password)
        if user is not None:
            login(request, user)
            if user.is_customer == True:
                return redirect('user:index')
            else:
                return redirect('user:login')
        else:
            return redirect('user:login')
    else :
        return render(request,"user/login.html")


# CUSTOMER REGISTRATION
def UserRegistration(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        country_code = request.POST['countryCode']
        phone = request.POST['Phone_number']
        phonenumber_with_countrycode = country_code + phone
        secret = pyotp.random_base32()
        if password == cpassword :
            customer = CutomerRegistration(email = email, phone_number = phonenumber_with_countrycode, password = password, name=name)
            customer.save()
            User = get_user_model()
            customers = User.objects.create_user(email=email,phone_number=phonenumber_with_countrycode, password=password,customer=customer, is_customer=True)

            profile = CutomerProfile.objects.create(user =customers,auth_token = secret)
            return redirect(f"/otp-page/{profile.test_id}")
        else:
            msg = "Password does not match"
            context = {
                'msg':msg,
            }
            return render(request,"user/registration.html",context)
    return render(request,"user/registration.html")


# PHONE NUMBER VALIDATION
@csrf_exempt
def checkPhoneNumber(request):
    phone = request.POST['phone']
    if User.objects.filter(phone_number=phone).exists():
        data = {
            "status":1,
            "msg": 'User Alreay Exists in the same phone number',
        }
        return JsonResponse(data)
    else:
        data ={
            "msg": '"user not exists',
            "status":0
        }
        return JsonResponse(data)


# SEND OTP
def otp_fun(request,id):
    profile = CutomerProfile.objects.get(test_id = id)
    totp = pyotp.TOTP(profile.auth_token,interval=300)
    otp = totp.now()
    if request.method == 'POST':
        enter_otp=request.POST['otp']
        verification = totp.verify(enter_otp)

        if verification == True:
            return redirect("user:index")
        else :
            pass
    message_handler=MessageHandler(profile.user.phone_number, otp).send_otp_on_phone()
    return render(request,"user/otp_generation.html",{'token':profile.test_id})


# forgot password
def forgot(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            if not User.objects.filter(email=email).first():
                messages.success(request, 'Not user found with this email.')
                return redirect('/forgot')
            else:
                pass
            user_obj = User.objects.get(email = email)
            token = str(uuid.uuid4())
            profile_obj= CutomerProfile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forgot')
    except Exception as e:
        print(e)
    return render(request,"user/forgot.html") 


# RESET PASSWORD
def resetPassword(request,token):
    context = {}
    try:
        profile_obj = CutomerProfile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST['password']
            user_id = request.POST.get('user_id')
            if user_id is  None:
                messages.warning(request, 'No user id found.')

                return redirect(f'/change-password/{token}/')
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()

            messages.success(request, 'An email sent')
            return redirect(f'/change-password/{token}/')
    except Exception as e:
        print(e)
    return render(request,"user/reset_password.html",context)


# RESEND OTP
def resendOtp(request , token):
    user = CutomerProfile.objects.filter(test_id = token).last()
    user_secret_key = pyotp.random_base32()
    user.auth_token = user_secret_key
    user.save()
    return redirect(f'/otp-page/{user.test_id}')


# DASHBOARD
def index(request):
    user_logout = request.user
    context = {
        "is_index" : True
    }
    return render(request,"user/index.html",context) 


# ABOUT
def about(request):
    return render(request,"user/about.html")


# CONTACT
def contact(request):
    return render(request,"user/contact.html")


# TERMS AND CONDITIONS
def termsAndConditions(request):
    return render(request,"user/terms-and-conditions.html")


# SELL YOUR PHONE
def sell(request):
    brand = Brand.objects.all()
    context = {
        "is_sellphone":True,
        "brand" : brand
    }
    return render(request,"user/sellphone.html",context)


# ACCOUNTS
def account(request):
    return render(request,"user/account.html")


# PRIVACY AND POLICY
def privacyAndPolicy(request):
    return render(request,"user/privacy-policy.html")


# BRAND MODELS
def shops(request,id):
    model = BrandModel.objects.filter(brand__id=id)
    context = {
        "model" : model
    }
    return render(request,"user/shops.html",context)    
    

# QUESTIONS
def question(request):
    return render(request,"user/question.html")  


# MODEL SPECIFICATIONS
def spec(request,id):
    # spec = ModelSpecifications.objects.filter(Brand_model__id=id)
    specification = BrandModel.objects.get(id=id)
    context = {
        "specification" : specification
    }
    return render(request,"user/spec-product.html",context)  


def getspecdata(request,id):
    spec_data = ModelSpecifications.objects.get(id=id)
    data = {
        'name':spec_data.Brand_model.name,
        'modelimage':spec_data.Brand_model.image.url,
        'ram':spec_data.RAM,
        'price':spec_data.price,
    }
    return JsonResponse(data)


# BUY PHONE
def buyPhone(request):
    context = {
        "is_buyphone":True
    }
    return render(request,"user/buyphone.html",context)  


# REPAIR PHONE
def repairPhone(request):
    context = {
        "is_repair":True
    }
    return render(request,"user/repairphone.html",context)  


# PAYMENT
# 
def payment(request):
    return render(request,"user/payment.html")      
 

# COMING SOON
def comingsoon(request):
    context = {
        "is_gadget":True,
        "is_newgadget":True
    }
    return render(request,"user/comingsoon.html",context)      


def handler404(request, exception):
    return render(request, "user/404.html", status=404)

# USER LOGOUT
def userLogout(request):
    user_logout = request.user
    logout(request)
    return redirect('user:index')


