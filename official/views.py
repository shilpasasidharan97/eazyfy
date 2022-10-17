from django.shortcuts import render

# Create your views here.

def base(request):
    return render(request,'official/partials/base.html')

def loginPage(request):
    return render(request,'official/login.html')


def forgotPassword(request):
    return render(request,'official/forgot_password.html')


def home(request):
    return render(request,'official/home.html')


def franchise(request):
    return render(request,'official/franchise.html')


def brand(request):
    return render(request,'official/brand.html')