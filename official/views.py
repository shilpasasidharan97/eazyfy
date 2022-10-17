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


def viewFranchiseDetails(request):
    return render(request,'official/view_franchise.html')


def brand(request):
    return render(request,'official/brand.html')


def Model(request):
    return render(request,'official/model.html')


def addModel(request):
    return render(request,'official/add_model.html')