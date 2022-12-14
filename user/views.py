import json
import uuid

from official.models import BannerImage
from official.models import Brand
from official.models import BrandModel
from official.models import CustomerProfile
from official.models import CustomerRegistration
from official.models import ModelSpecifications
from official.models import Offer
from official.models import Question, UserReply, UserRequest, QuestionOption
from official.models import User
from user.mixin import MessageHandler

import pyotp
from .helpers import send_forget_password_mail
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# CUSTOMER LOGIN
def customerlogin(request):
    if request.method == "POST":
        countryCode = request.POST["countryCode"]
        number = request.POST["number"]
        login_countryCode = countryCode + number
        password = request.POST["password"]
        user = authenticate(request, phone_number=login_countryCode, password=password)
        if user is not None:
            login(request, user)
            if user.is_customer:
                return redirect("user:index")
            return redirect("user:login")
        return redirect("user:login")
    else:
        return render(request, "user/login.html")


# CUSTOMER REGISTRATION
def UserRegistration(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]
        country_code = request.POST["countryCode"]
        phone = request.POST["Phone_number"]
        phonenumber_with_countrycode = country_code + phone
        secret = pyotp.random_base32()
        if password == cpassword:
            customer = CustomerRegistration(email=email, phone_number=phonenumber_with_countrycode, password=password, name=name)
            customer.save()
            User = get_user_model()
            customers = User.objects.create_user(email=email, phone_number=phonenumber_with_countrycode, password=password, customer=customer, is_customer=True)
            profile = CustomerProfile.objects.create(user=customers, auth_token=secret)
            return redirect(f"/otp-page/{profile.test_id}")
        msg = "Password does not match"
        context = {"msg": msg}
        return render(request, "user/registration.html", context)
    return render(request, "user/registration.html")


# PHONE NUMBER VALIDATION
@csrf_exempt
def checkPhoneNumber(request):
    phone = request.POST["phone"]
    if User.objects.filter(phone_number=phone).exists():
        data = {"status": 1, "msg": "User Alreay Exists in the same phone number"}
        return JsonResponse(data)
    data = {"msg": '"user not exists', "status": 0}
    return JsonResponse(data)


# SEND OTP
def otp_fun(request, id):
    profile = CustomerProfile.objects.get(test_id=id)
    totp = pyotp.TOTP(profile.auth_token, interval=300)
    otp = totp.now()
    if request.method == "POST":
        enter_otp = request.POST["otp"]
        verification = totp.verify(enter_otp)
        if verification:
            return redirect("user:index")
    MessageHandler(profile.user.phone_number, otp).send_otp_on_phone()
    return render(request, "user/otp_generation.html", {"token": profile.test_id})


# forgot password
def forgot(request):
    if request.method == "POST":
        email = request.POST["email"]
        if not User.objects.filter(email=email).first():
            messages.success(request, "Not user found with this email.")
            return redirect("/forgot")
        user_obj = User.objects.get(email=email)
        token = str(uuid.uuid4())
        profile_obj = CustomerProfile.objects.get(user=user_obj)
        profile_obj.forget_password_token = token
        profile_obj.save()
        send_forget_password_mail(user_obj.email, token)
        messages.success(request, "An email is sent.")
        return redirect("/forgot")
    return render(request, "user/forgot.html")


# RESET PASSWORD
def resetPassword(request, token):
    profile_obj = CustomerProfile.objects.filter(forget_password_token=token).first()
    context = {"user_id": profile_obj.user.id}
    if request.method == "POST":
        new_password = request.POST["password"]
        user_id = request.POST.get("user_id")
        if user_id is None:
            messages.warning(request, "No user id found.")

            return redirect(f"/change-password/{token}/")
        user_obj = User.objects.get(id=user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        messages.success(request, "An email sent")
        return redirect(f"/change-password/{token}/")
    return render(request, "user/reset_password.html", context)


# RESEND OTP
def resendOtp(request, token):
    user = CustomerProfile.objects.filter(test_id=token).last()
    user_secret_key = pyotp.random_base32()
    user.auth_token = user_secret_key
    user.save()
    return redirect(f"/otp-page/{user.test_id}")


# DASHBOARD
def index(request):
    banner = BannerImage.objects.all()
    offer = Offer.objects.all()
    brand = Brand.objects.all()
    user = request.user
    context = {"is_index": True, "user": user, "banner": banner, "offer": offer, "brand": brand}
    return render(request, "user/index.html", context)


# ABOUT
def about(request):
    return render(request, "user/about.html")


# CONTACT
def contact(request):
    return render(request, "user/contact.html")


# TERMS AND CONDITIONS
def termsAndConditions(request):
    return render(request, "user/terms-and-conditions.html")


# SELL YOUR PHONE
def sell(request):
    brand = Brand.objects.all()
    context = {"is_sellphone": True, "brand": brand}
    return render(request, "user/sellphone.html", context)


# ACCOUNTS
def account(request):
    return render(request, "user/account.html")


# PRIVACY AND POLICY
def privacyAndPolicy(request):
    return render(request, "user/privacy-policy.html")


# BRAND MODELS
def shops(request, id):
    model = BrandModel.objects.filter(brand__id=id)
    searchModel = BrandModel.objects.filter(brand__id=id)
    data = []
    for pos in searchModel:
        item = {"pk": pos.pk, "modelName": pos.name}
        data.append(item)
    context = {"data": data, "searchModel": searchModel, "model": model}
    return render(request, "user/shops.html", context)


@login_required
def question(request, id):
    spec = ModelSpecifications.objects.get(id=id)
    questions = Question.objects.all()
    user_request = UserRequest.objects.get_or_create(user=request.user, phonemodel=spec, is_submitted=False)[0]
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
    context = {"spec": spec, "questions": questions, "replies": replies, "user_request": user_request}
    return render(request, "user/question.html", context)


@csrf_exempt
def save_answer(request):
    json.loads(request.POST["data"])
    return JsonResponse({"msg": "Success"})


# MODEL SPECIFICATIONS
def spec(request, id):
    specification = BrandModel.objects.get(id=id)
    context = {"specification": specification, "id": id}
    return render(request, "user/spec-product.html", context)


def getspecdata(request, id):
    spec_data = ModelSpecifications.objects.get(id=id)
    data = {"name": spec_data.brand_model.name, "modelimage": spec_data.brand_model.image.url, "ram": spec_data.RAM, "price": spec_data.price}
    return JsonResponse(data)


# BUY PHONE
def buyPhone(request):
    brand = Brand.objects.all()
    context = {"is_buyphone": True, "brand": brand}
    return render(request, "user/buyphone.html", context)


# REPAIR PHONE
def repairPhone(request):
    context = {"is_repair": True}
    return render(request, "user/repairphone.html", context)


def payment(request):
    return render(request, "user/payment.html")


# COMING SOON
def comingsoon(request):
    context = {"is_gadget": True}
    return render(request, "user/comingsoon.html", context)


def findnewgadget(request):
    context = {"is_newgadget": True}
    return render(request, "user/findnewgadget.html", context)


def sellPhone(request):
    brand = Brand.objects.all()
    data = []
    for pos in brand:
        item = {"pk": pos.pk, "brandName": pos.name}
        data.append(item)
    context = {"data": data, "brand": brand}
    return render(request, "user/sell-phone.html", context)


def handler404(request, exception):
    return render(request, "user/404.html", status=404)


def userLogout(request):
    logout(request)
    return redirect("user:index")
