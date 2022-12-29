from eazyfy.decorators import auth_pickupboy
from official.models import OrderPayment
from official.models import PickUpBoy

import razorpay
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render


def base(request):
    return render(request, "pickup-boy/partials/base.html")


# PROFILE AND PROFILE EDITING
@auth_pickupboy
@login_required(login_url="/official/loginpage")
def profile(request):
    pickupboy = request.user.pickup_boy
    if request.method == "POST":
        print("post")
        name = request.POST["pname"]
        phone = request.POST["pphone"]
        email = request.POST["pemail"]
        address = request.POST["paddress"]
        photo = request.FILES["pphoto"]

        PickUpBoy.objects.filter(id=pickupboy.id).update(name=name, phone=phone, email=email, address=address)
        photo_pb = PickUpBoy.objects.get(id=pickupboy.id)
        photo_pb.photo = photo
        photo_pb.save()
        print("qwerty")
        get_user_model().objects.filter(pickup_boy=pickupboy.id).update(phone_number=phone, email=email)
        return redirect("pickupboy:profile")
    context = {"pickupboy": pickupboy}
    return render(request, "pickup-boy/profile.html", context)


# DASHBOARD
@auth_pickupboy
@login_required(login_url="/official/loginpage")
def index(request):
    context = {"is_index": True}
    return render(request, "pickup-boy/index.html", context)


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def complete_selfy(request):
    return render(request, "pickup-boy/complete-selfy.html")


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def total_order(request):
    context = {"is_order": True}
    return render(request, "pickup-boy/total-order.html", context)


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def product_details(request):
    return render(request, "pickup-boy/product-details.html")


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def verification_questions(request):
    return render(request, "pickup-boy/verification-questions.html")


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def complete(request):
    return render(request, "pickup-boy/complete.html")


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def customer_selfy(request):
    return render(request, "pickup-boy/customer-selfy.html")


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def fail(request):
    return render(request, "pickup-boy/fail.html")


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def requote(request):
    return render(request, "pickup-boy/requote.html")


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def requote_selfy(request):
    return render(request, "pickup-boy/requote-selfy.html")


# @auth_pickupboy
# @login_required(login_url='/official/loginpage')
def checkout(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = int(request.POST.get("amount")) * 100
        client = razorpay.Client(auth=("rzp_test_bKtMj90QOs6Af2", "vNLvdBnrIGSHG2C4BiWoDGvd"))
        payment = client.order.create({"amount": amount, "currency": "INR", "payment_capture": "1"})
        print(payment)
        coffe = OrderPayment(name=name, amound=amount, paiment_id=payment["id"])
        return render(request, "pickup-boy/checkout.html", {"payment": payment})
    return render(request, "pickup-boy/checkout.html")
