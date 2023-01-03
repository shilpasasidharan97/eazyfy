from eazyfy.decorators import auth_franchise
from official.models import AdminSendRecord
from official.models import Franchise
from official.models import PickUpBoy

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="/official/loginpage")
@auth_franchise
def header(request):
    franchise = request.user.franchise
    context = {"franchise": franchise}
    return render(request, "franchise/header.html", context)


# DASHBOARD
@auth_franchise
@login_required(login_url="/official/loginpage")
def index(request):
    franchise = request.user.franchise
    payment_from_admin = AdminSendRecord.objects.filter(franchise=franchise).order_by("date")
    pickup_boy_list = PickUpBoy.objects.filter(franchise=franchise).order_by("name")
    count = pickup_boy_list.count()

    total_amount = 0
    for i in payment_from_admin:
        total_amount += i.amount

    context = {"franchise": franchise, "is_index": True, "payment_from_admin": payment_from_admin, "total_amount": total_amount, "count": count}
    return render(request, "franchise/index.html", context)


# PICK-UP BOY ADDING
@auth_franchise
@login_required(login_url="/official/loginpage")
def add_pickupboy(request):
    franchise = request.user.franchise
    if request.method == "POST":
        name = request.POST["name"]
        pickup_boy_id = request.POST["pickup_boy_id"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        password = request.POST["password"]
        place = request.POST["place"]
        address = request.POST["address"]
        photo = request.FILES["photo"]

        pickup_boy = PickUpBoy(franchise=franchise, pickup_id=pickup_boy_id, name=name, email=email, phone=phone, photo=photo, place=place, address=address, password=password)
        pickup_boy.save()

        User = get_user_model()
        User.objects.create_user(phone_number=phone, password=password, pickup_boy=pickup_boy, is_pickupboy=True)
        return redirect("franchise:add-pickupboy")
    pickup_boy_list = PickUpBoy.objects.filter(franchise=franchise).order_by("name")
    context = {"is_addpickupboy": True, "pickup_boy_list": pickup_boy_list}
    return render(request, "franchise/add-pickupboy.html", context)


# EDITDATA OF PICKUPBOY
@csrf_exempt
def getprofiledata(request, id):
    details = PickUpBoy.objects.get(id=id)
    data = {
        "id": details.id,
        "pid": details.pickup_id,
        "name": details.name,
        "email": details.email,
        "phone": details.phone,
        "place": details.place,
        "address": details.address,
        # "photo": details.photo.url,
    }
    return JsonResponse({"value": data})


# PICKUPBOY EDITING
@csrf_exempt
def editform(request, id):
    pid = request.POST["pid"]
    pname = request.POST["pname"]
    pemail = request.POST["pemail"]
    pickupboyphone = request.POST["pickupboyphone"]
    pickupboyplace = request.POST["pickupboyplace"]
    paddress = request.POST["paddress"]

    PickUpBoy.objects.filter(id=id).update(pickup_id=pid, name=pname, email=pemail, phone=pickupboyphone, place=pickupboyplace, address=paddress)
    get_user_model().objects.filter(pickup_boy=id).update(phone_number=pickupboyphone, email=pemail)
    data = {"ss": "csac"}
    return JsonResponse(data)


# DELETE PICKUPBOY
def Deletepickupboy(request, id):
    PickUpBoy.objects.get(id=id).delete()
    return redirect("/franchise/add-pickupboy")


# PROFILE AND PROFILE EDITING
@auth_franchise
@login_required(login_url="/official/loginpage")
def profile(request):
    franchise = request.user.franchise
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        address = request.POST["address"]
        photo = request.FILES["fphoto"]

        Franchise.objects.filter(id=franchise.id).update(name=name, phone=phone, email=email, address=address)
        photo_fr = Franchise.objects.get(id=franchise.id)
        photo_fr.photo = photo
        photo_fr.save()
        get_user_model().objects.filter(franchise=franchise.id).update(phone_number=phone, email=email)
        return redirect("franchise:profile")
    context = {"franchise": franchise}
    return render(request, "franchise/profile.html", context)


# ORDER LIST
@auth_franchise
@login_required(login_url="/official/loginpage")
def order(request):
    context = {"is_order": True}
    return render(request, "franchise/order.html", context)


@auth_franchise
@login_required(login_url="/official/loginpage")
def transactions(request):
    franchise = request.user.franchise
    payment_from_admin = AdminSendRecord.objects.filter(franchise=franchise).order_by("date")
    context = {"payment_from_admin": payment_from_admin}
    return render(request, "franchise/transactions.html", context)
