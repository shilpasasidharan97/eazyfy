from django.shortcuts import render
from official.models import *

# Create your views here.

def base(request):
    return render(request,"pickup-boy/partials/base.html")



def profile(request):
    return render(request,"pickup-boy/profile.html")

def index(request):
    print(request.user.pickup_boy.name)
    return render(request,"pickup-boy/index.html")

def complete_selfy(request):
    return render(request,"pickup-boy/complete-selfy.html")

def total_order(request):
    return render(request,"pickup-boy/total-order.html")

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