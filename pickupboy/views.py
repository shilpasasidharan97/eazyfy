from django.shortcuts import render
from official.models import *
from eazyfy.decorators import auth_pickupboy
from django.contrib.auth.decorators import login_required


# Create your views here.


@auth_pickupboy
@login_required(login_url='/official/loginpage')
def base(request):
    return render(request,"pickup-boy/partials/base.html")


# PROFILE
@auth_pickupboy
@login_required(login_url='/official/loginpage')
def profile(request):
    return render(request,"pickup-boy/profile.html")


@auth_pickupboy
@login_required(login_url='/official/loginpage')
def index(request):
    context ={
        "is_index":True
    }
    return render(request,"pickup-boy/index.html",context)


@auth_pickupboy
@login_required(login_url='/official/loginpage')
def complete_selfy(request):
    return render(request,"pickup-boy/complete-selfy.html")


@auth_pickupboy
@login_required(login_url='/official/loginpage')
def total_order(request):
    context = {
        "is_order":True
    }
    return render(request,"pickup-boy/total-order.html",context)


@auth_pickupboy
@login_required(login_url='/official/loginpage')
def product_details(request):
    return render(request,"pickup-boy/product-details.html")


@auth_pickupboy
@login_required(login_url='/official/loginpage')
def verification_questions(request):
    return render(request,"pickup-boy/verification-questions.html")


@auth_pickupboy
@login_required(login_url='/official/loginpage')
def complete(request):
    return render(request,"pickup-boy/complete.html")


@auth_pickupboy
@login_required(login_url='/official/loginpage')
def customer_selfy(request):
    return render(request,"pickup-boy/customer-selfy.html")


@auth_pickupboy
@login_required(login_url='/official/loginpage')
def fail(request):
    return render(request,"pickup-boy/fail.html")


@auth_pickupboy
@login_required(login_url='/official/loginpage')
def requote(request):
    return render(request,"pickup-boy/requote.html")


@auth_pickupboy
@login_required(login_url='/official/loginpage')
def requote_selfy(request):
    return render(request,"pickup-boy/requote-selfy.html")


# edit

# @csrf_exempt
# def editboy(request,id):
#     pickup_id = request.POST['pid']
#     name = request.POST['pname']
#     email = request.POST['pemail']
#     phone = request.POST['pphone']
#     franchise = request.POST['pfranchise']
#     address = request.POST['paddress']
#     address = request.POST['paddress']
#     photo = request.FILES['pphone']
#     place = request.POST['plocation']
#     PickUpBoy.objects.filter(id=id).update(pickup_id=pickup_id, name=name, email=email, phone=phone, address=address,franchise=franchise,photo=photo,place=place)
#     # get_user_model().objects.filter(franchise__id=id).update(phone_number=phone,email=email)
#     data ={
#         "ss":"csac",
#     }
#     return JsonResponse(data)