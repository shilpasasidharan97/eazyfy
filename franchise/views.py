from eazyfy.decorators import auth_franchise
from official.models import Franchise, FranchiseWallet
from official.models import PickUpBoy
from official.models import UserRequest

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import PickupAssignForm
from django.contrib import messages


@auth_franchise
@login_required(login_url="/official/loginpage")
def index(request):
    franchise = request.user.franchise
    incomes = FranchiseWallet.objects.filter(franchise=franchise, type="to_franchise")
    expenses = FranchiseWallet.objects.filter(franchise=franchise, type="to_admin")
    context = {"franchise": franchise, "is_index": True, "incomes": incomes, "expenses": expenses}
    return render(request, "franchise/index.html", context)


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

        pickup_boy = PickUpBoy(
            franchise=franchise,
            pickup_id=pickup_boy_id,
            name=name,
            email=email,
            phone=phone,
            photo=photo,
            place=place,
            address=address,
            password=password,
        )
        pickup_boy.save()

        User = get_user_model()
        User.objects.create_user(phone_number=phone, password=password, pickup_boy=pickup_boy, is_pickupboy=True)
        return redirect("franchise:add-pickupboy")
    pickup_boy_list = PickUpBoy.objects.filter(franchise=franchise).order_by("name")
    context = {"is_addpickupboy": True, "pickup_boy_list": pickup_boy_list}
    return render(request, "franchise/add-pickupboy.html", context)


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
    }
    return JsonResponse({"value": data})


@csrf_exempt
def editform(request, id):
    pid = request.POST["pid"]
    pname = request.POST["pname"]
    pemail = request.POST["pemail"]
    pickupboyphone = request.POST["pickupboyphone"]
    pickupboyplace = request.POST["pickupboyplace"]
    paddress = request.POST["paddress"]

    PickUpBoy.objects.filter(id=id).update(
        pickup_id=pid, name=pname, email=pemail, phone=pickupboyphone, place=pickupboyplace, address=paddress
    )
    get_user_model().objects.filter(pickup_boy=id).update(phone_number=pickupboyphone, email=pemail)
    data = {"ss": "csac"}
    return JsonResponse(data)


def Deletepickupboy(request, id):
    PickUpBoy.objects.get(id=id).delete()
    return redirect("/franchise/add-pickupboy")


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


@auth_franchise
@login_required(login_url="/official/loginpage")
def order(request):
    franchise = request.user.franchise
    requests = UserRequest.objects.filter(is_submitted=True, is_assigned_to_franchise=True, franchise=franchise)
    self_assigned_requests = requests.filter(is_assigned_to_pickup=True)
    context = {"is_request": True, "self_assigned_requests": self_assigned_requests, "requests": requests}
    return render(request, "franchise/order.html", context)


@auth_franchise
@login_required(login_url="/official/loginpage")
def transactions(request):
    franchise = request.user.franchise
    transactions = FranchiseWallet.objects.filter(franchise=franchise).order_by("date")
    context = {"transactions": transactions}
    return render(request, "franchise/transactions.html", context)


@auth_franchise
@login_required(login_url="/official/loginpage")
def order_details(request, id):
    request_details = UserRequest.objects.get(id=id)
    form = PickupAssignForm(request.POST or None, instance=request_details)
    form.fields["pickupboy"].queryset = PickUpBoy.objects.filter(franchise=request.user.franchise)
    if request.method == "POST":
        if form.is_valid():
            data = form.save()
            data.is_assigned_to_franchise = True
            data.save()
            messages.success(request, "Request Assigned Successfully")
            return redirect("franchise:order")
    context = {"is_order_details": True, "request_details": request_details, "form": form}
    return render(request, "franchise/order_details.html", context)


@auth_franchise
@login_required(login_url="/official/loginpage")
def accept_order(request, id):
    request_details = UserRequest.objects.get(id=id)
    request_details.is_franchise_accepted = True
    request_details.save()
    return JsonResponse({"status": "success"})
