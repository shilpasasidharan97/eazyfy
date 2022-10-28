from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request,"user/partials/base.html") 

def index(request):
    return render(request,"user/index.html") 

def about(request):
    return render(request,"user/about.html")

def contact(request):
    return render(request,"user/contact.html")

def termsAndConditions(request):
    return render(request,"user/terms-and-conditions.html.html")

def login(request):
    return render(request,"user/login.html")

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