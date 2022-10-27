from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
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


@login_required(login_url='/official/loginpage')
def home(request):
    return render(request,'official/home.html')


@login_required(login_url='/official/loginpage')
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
        return redirect('official:franchise')
    else:
        franchise_list = Franchise.objects.all().order_by('name')
        context={
            "franchise_list" : franchise_list
        }
        return render(request,'official/franchise.html',context)


def viewFranchiseDetails(request,id):
    franchise_details = Franchise.objects.get(id=id)
    pickup_boys = PickUpBoy.objects.filter(franchise=franchise_details)
    context ={
        "franchise_details":franchise_details,
        "pickup_boys":pickup_boys,
    }
    return render(request,'official/view_franchise.html',context)


def DeleteFranchise(request,id):
    print("#"*20)
    Franchise.objects.get(id=id).delete()
    return redirect('/official/franchise')


def pickUpBoyList(request,id):
    franchise_details = Franchise.objects.get(id=id)
    return render(request,'official/pickupboy_list.html')


def brand(request):
    brands = Brand.objects.all().order_by('name')
    if request.method == 'POST':
        name = request.POST['name']
        photo = request.FILES['photo']
        new_brand = Brand(name=name, image=photo)
        new_brand.save()
    context = {
        "brands":brands,
    }
    return render(request,'official/brand.html', context)


def Model(request,id):
    brand = Brand.objects.get(id=id)
    models = BrandModel.objects.filter(brand=brand)
    if request.method == 'POST':
        brand = brand
        name =request.POST['name']
        image =request.FILES['image']
        
        new_model = BrandModel(brand=brand, image=image, name=name)
        new_model.save()
    context = {
        "models":models,
        "brand":brand
    }
    return render(request,'official/model.html', context)


def modelSpecification(request,id):
    brand = BrandModel.objects.get(brand=id)
    models_spec = ModelSpecifications.objects.filter(Brand_model=brand)
    if request.method == 'POST':
        brand = brand
        ram =request.POST['ram']
        internal_storage =request.POST['internal_storage']
        year =request.POST['year']
        color =request.POST['color']
        price = request.POST['price']
        
        new_model = ModelSpecifications(Brand_model=brand, RAM=ram, color=color, internal_storage=internal_storage, year=year, price=price)
        new_model.save()
    context = {
        "models_spec":models_spec,
    }
    return render(request,'official/specification.html', context)


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


def logout_view(request):
    logout(request)
    return redirect('/official/loginpage')

