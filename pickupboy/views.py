from flypik.decorators import auth_pickupboy
from official.models import OrderPayment
from official.models import PickUpBoy
from official.models import PickupData
from official.models import Question
from official.models import QuestionOption
from official.models import UserReply
from official.models import UserRequest

import razorpay
from .forms import PickupCompleteForm
from .forms import PickupFailForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def profile(request):
    pickupboy = request.user.pickup_boy
    if request.method == "POST":
        name = request.POST["pname"]
        phone = request.POST["pphone"]
        email = request.POST["pemail"]
        address = request.POST["paddress"]
        photo = request.FILES["pphoto"]

        PickUpBoy.objects.filter(id=pickupboy.id).update(name=name, phone=phone, email=email, address=address)
        photo_pb = PickUpBoy.objects.get(id=pickupboy.id)
        photo_pb.photo = photo
        photo_pb.save()
        get_user_model().objects.filter(pickup_boy=pickupboy.id).update(phone_number=phone, email=email)
        return redirect("pickupboy:profile")
    context = {"pickupboy": pickupboy}
    return render(request, "pickup-boy/profile.html", context)


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def index(request):
    pickupboy = request.user.pickup_boy
    requests = UserRequest.objects.filter(
        is_submitted=True,
        is_assigned_to_franchise=True,
        pickupboy=pickupboy,
        is_franchise_accepted=True,
        franchise=pickupboy.franchise,
    )
    context = {
        "is_order": True,
        "requests": requests,
        "pending_requests": requests.filter(status="pending"),
        "complete_requests": requests.filter(status="complete"),
        "requote_requests": requests.filter(status="requote"),
        "fail_requests": requests.filter(status="fail"),
    }
    return render(request, "pickup-boy/index.html", context)


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def total_order(request):
    pickupboy = request.user.pickup_boy
    requests = UserRequest.objects.filter(
        is_submitted=True,
        is_assigned_to_franchise=True,
        pickupboy=pickupboy,
        is_franchise_accepted=True,
        franchise=pickupboy.franchise,
    )
    context = {
        "is_order": True,
        "requests": requests,
        "pending_requests": requests.filter(status="pending"),
        "complete_requests": requests.filter(status="complete"),
        "requote_requests": requests.filter(status="requote"),
        "fail_requests": requests.filter(status="fail"),
    }
    return render(request, "pickup-boy/total-order.html", context)


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def product_details(request, id):
    request_details = UserRequest.objects.get(id=id)
    pickup_data, _ = PickupData.objects.get_or_create(user_request=request_details)
    context = {"request_details": request_details, "pickup_data": pickup_data}
    return render(request, "pickup-boy/order_details.html", context)


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def complete(request, id):
    request_details = UserRequest.objects.get(id=id)
    pickup_data, _ = PickupData.objects.get_or_create(user_request=request_details)
    form = PickupCompleteForm(request.POST or None, request.FILES or None, instance=pickup_data)
    if form.is_valid():
        form.save()
        request_details.status = "completed"
        request_details.status = "completed"
        request_details.save()
        return redirect("pickupboy:checkout", id=id)
    context = {"request_details": request_details, "form": form, "pickup_data": pickup_data}
    return render(request, "pickup-boy/complete.html", context)


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def fail(request, id):
    request_details = UserRequest.objects.get(id=id)
    pickup_data, _ = PickupData.objects.get_or_create(user_request=request_details)
    form = PickupFailForm(request.POST or None, request.FILES or None, instance=pickup_data)
    context = {"request_details": request_details, "form": form, "pickup_data": pickup_data}
    if form.is_valid():
        form.save()
        request_details.status = "failed"
        pickup_data.status = "failed"
        request_details.save()
        return redirect("pickupboy:total_order")
    return render(request, "pickup-boy/fail.html", context)


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def requote_first(request, id):
    user_request = UserRequest.objects.get(id=id)
    variant = user_request.phonemodel
    questions = Question.objects.all()
    replies = UserReply.objects.filter(user_request=user_request)
    if request.method == "POST":
        data = dict(request.POST.items())
        data.pop("csrfmiddlewaretoken")
        for key, value in data.items():
            question = Question.objects.get(id=key)
            option = QuestionOption.objects.get(id=value)
            if UserReply.objects.filter(user_request=user_request, question=question).exists():
                answer = UserReply.objects.get(user_request=user_request, question=question)
                answer.option = option
            else:
                answer = UserReply.objects.create(question=question, option=option, user_request=user_request)
            answer.save()
        return redirect("pickupboy:requote_next", id=user_request.id)
    context = {"variant": variant, "questions": questions, "replies": replies, "user_request": user_request}
    return render(request, "pickup-boy/requote_first.html", context)


@auth_pickupboy
@login_required(login_url="/official/loginpage")
def requote_next(request, id):
    request_details = UserRequest.objects.get(id=id)
    pickup_data, _ = PickupData.objects.get_or_create(user_request=request_details)
    form = PickupCompleteForm(request.POST or None, request.FILES or None, instance=pickup_data)
    if form.is_valid():
        form.save()
        request_details.status = "requote"
        request_details.save()
        return redirect("pickupboy:total_order")
    context = {"request_details": request_details, "form": form, "pickup_data": pickup_data}
    return render(request, "pickup-boy/requote_next.html", context)


def checkout(request, id):
    request_details = UserRequest.objects.get(id=id)
    pickup_data, _ = PickupData.objects.get_or_create(user_request=request_details)
    context = {"request_details": request_details, "pickup_data": pickup_data}
    if request.method == "POST":
        name = request.POST.get("name")
        client = razorpay.Client(auth=("rzp_test_bKtMj90QOs6Af2", "vNLvdBnrIGSHG2C4BiWoDGvd"))
        payment = client.order.create(
            {"amount": request_details.final_amount, "currency": "INR", "payment_capture": "1"}
        )
        coffe = OrderPayment(name=name, amount=request_details.final_amount, payment_id=payment["id"])
        return render(
            request,
            "pickup-boy/checkout.html",
            {"payment": payment, "coffe": coffe, "request_details": request_details},
        )
    return render(request, "pickup-boy/checkout.html", context)
