from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from .models import *

# Create your views here.

def base(request):
    return render(request,'official/partials/base.html')

def loginPage(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        user = authenticate(phone_number=phone, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser == True:
                return redirect('official:home')
            elif user.is_franchise == True:
                return redirect('franchise:index')
            elif user.is_pickupboy == True:
                return redirect('pickupboy:index')
            # elif user.Student !=None:
            #     return redirect('student:home')
        else:
            msg = "* Incorrect email or password *"
            return render(request,'official/login.html',{'msg':msg,})
    return render(request,'official/login.html')


def forgotPassword(request):
    return render(request,'official/forgot_password.html')


def home(request):
    return render(request,'official/home.html')


def franchise(request):
    
    
    if request.method == 'POST':
        
        name = request.POST['name']
        franchise_id = request.POST['franchise_id']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        photo = request.FILES['photo']
        franchise = Franchise(name=name, franchise_id=franchise_id, email=email, phone=phone, photo=photo, address=address, password=password)
        franchise.save()

        User = get_user_model()
        User.objects.create_user(phone_number=phone, password=password,franchise=franchise, is_franchise=True)
        return render(request,'official/franchise.html')
    else:
        franchise_list = Franchise.objects.all().order_by('name')
        context={
            "franchise_list" : franchise_list
        }
        return render(request,'official/franchise.html',context)


def viewFranchiseDetails(request):
    
    return render(request,'official/view_franchise.html')


def pickUpBoyList(request):
    return render(request,'official/pickupboy_list.html')


def brand(request):
    return render(request,'official/brand.html')


def Model(request):
    return render(request,'official/model.html')


def modelSpecification(request):
    return render(request,'official/specification.html')


def questionAdding(request):
    return render(request,'official/questions_adding.html')


def userRequestList(request):
    return render(request,'official/user_request.html')


def userDetails(request):
    return render(request,'official/view_userdetails.html')


def transactionHistory(request):
    return render(request,'official/transaction_history.html')


def wallet(request):
    return render(request,'official/wallet.html')

def profile(request):
    return render(request,'official/profile.html')