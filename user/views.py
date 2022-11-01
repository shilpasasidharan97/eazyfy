from django.shortcuts import render, redirect
import pyotp
from user.mixin import *
from official.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login



def customerlogin(request):
    if request.method == 'POST':
        # print('post'*20)
        number = request.POST['number']
        password = request.POST['password']
        print(number,"#"*20)
        print(password,"$"*20)
        user = authenticate(request,phone_number=number, password=password)
        print(user)
        if user is not None:
            print('firstif'*20)
            login(request, user)
            if user.is_customer == True:
               
                return redirect('user:about')
            else:
                return redirect('user:login')
        else:
            print('eroor')
    return render(request,"user/login.html")

# Create your views here.
def UserRegistration(request):
    # if request.method == 'POST':
    #     number = request.POST['number']
    #     password = request.POST['password']
    #     user = authenticate(phone_number=number, password=password)
    #     if user is not None:
    #         login(request, user)
    #         if user.is_superuser == True:
    #             return redirect('user:about')
    #         else:
    #             pass
    print("GEEETTTT")
    if request.method == 'POST':
        print('POOOOSSSTTTTT')
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        phone = request.POST['Phone_number']
        secret = pyotp.random_base32() 
        print('@'*20)
        # if password == cpassword :
        
        customer = CutomerRegistration(email = email, phone_number = phone, password = password)
        customer.save()
        User = get_user_model()
        customers = User.objects.create_user(phone_number=phone, password=password,customer=customer, is_customer=True)

        profile = CutomerProfile.objects.create(user =customers,auth_token = secret)
        # print('#'*20)
        
        print(profile.test_id)
        return redirect(f"/otp-page/{profile.test_id}")
        # return redirect('/user/otp/'+str(profile.id))

    
    return render(request,"user/registration.html")


def otp_fun(request,id):
    print("#"*20)
    profile = CutomerProfile.objects.get(test_id = id)

    print(profile.user.phone_number)
    totp = pyotp.TOTP(profile.auth_token,interval=300)
    otp = totp.now()
    print("otp",otp) 

    if request.method == 'POST':
        enter_otp=request.POST['otp']
        print("enter otp",enter_otp)
        verification = totp.verify(enter_otp)

        if verification == True:
            return redirect("user:index")
        else :
            print("failed")
    message_handler=MessageHandler(profile.user.phone_number, otp).send_otp_on_phone()
    return render(request,"user/otp_generation.html")




def index(request):
    return render(request,"user/index.html") 

def about(request):
    return render(request,"user/about.html")

def contact(request):
    return render(request,"user/contact.html")

def termsAndConditions(request):
    return render(request,"user/terms-and-conditions.html")



def sell(request):
    return render(request,"user/sellphone.html")

def account(request):
    return render(request,"user/account.html")

def privacy(request):
    return render(request,"user/privacy.html")

def shops(request):
    return render(request,"user/shops.html")    
    
def question(request):
    return render(request,"user/question.html")  

def my(request):
    return render(request,"user/my.html")  

def spec(request):
    return render(request,"user/spec-product.html")  

def buy(request):
    return render(request,"user/buyphone.html")  

def repair(request):
    return render(request,"user/repairphone.html")  
def payment(request):
    return render(request,"user/payment.html")      


def registration(request):

    return render(request,"web/registration.html")