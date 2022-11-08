from django.shortcuts import render,redirect
from official.models import *
from django.contrib.auth import get_user_model

# Create your views here.

def base(request):
    return render(request,"pickup-boy/partials/base.html")

def profile(request):
    pickupboy = request.user.pickup_boy
    print(pickupboy)

    if request.method == 'POST':
        print('post')
        name = request.POST['pname']
        phone = request.POST['pphone']
        email = request.POST['pemail']
        address = request.POST['paddress']
        photo = request.FILES['pphoto']

        PickUpBoy.objects.filter(id=pickupboy.id).update(name=name, phone=phone, email=email,address=address)
        photo_pb = PickUpBoy.objects.get(id=pickupboy.id)
        photo_pb.photo=photo
        photo_pb.save()
        print("qwerty")
        get_user_model().objects.filter(pickup_boy=pickupboy.id).update(phone_number=phone, email=email)
         
        return redirect('pickupboy:profile')

    context = {
        "pickupboy":pickupboy,
    }

    return render(request,"pickup-boy/profile.html",context)

def index(request):
    context ={
        "is_index":True
    }
    return render(request,"pickup-boy/index.html",context)

def complete_selfy(request):
    return render(request,"pickup-boy/complete-selfy.html")

def total_order(request):
    context = {
        "is_order":True
    }
    return render(request,"pickup-boy/total-order.html",context)

def product_details(request):
    return render(request,"pickup-boy/product-details.html")

def verification_questions(request):
    return render(request,"pickup-boy/verification-questions.html")

def complete(request):
    return render(request,"pickup-boy/complete.html")

def customer_selfy(request):
    return render(request,"pickup-boy/customer-selfy.html")

def fail(request):
    return render(request,"pickup-boy/fail.html")

def requote(request):
    return render(request,"pickup-boy/requote.html")

def requote_selfy(request):
    return render(request,"pickup-boy/requote-selfy.html")


# edit pickupboy

# def profile(request):
   

        # PickUpBoy.objects.filter(id=pickupboy.id).update(name=name, phone=phone, email=email, address=address)
        # photo_fr = PickUpBoy.objects.get(id=pickupboy.id)
        # photo_fr.photo=photo
        # photo_fr.save()
        # print("qwerty")
        # get_user_model().objects.filter(pickupboy=pickupboy.id).update(phone_number=phone, email=email)
        # print("55"*20)
        # return redirect('pickupboy:profile')
