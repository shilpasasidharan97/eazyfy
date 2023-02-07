from official.models import Customer
from official.models import Question
from official.models import QuestionOption
from official.models import User
from official.models import UserReply
from official.models import UserRequest
from official.models import Variant
from main.forms import PhoneOTPForm
from .forms import UserRequestInfoForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from main.models import PhoneOTP
import random
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages


@login_required
def question(request, id):
    variant = Variant.objects.get(id=id)
    questions = Question.objects.all()
    if request.user.usertype == "customer" and not Customer.objects.filter(user=request.user).exists():
        customer = Customer(user=request.user).save()
    customer = request.user.customer
    user_request = UserRequest.objects.get_or_create(customer=customer, phonemodel=variant, is_submitted=False)[0]
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
        return redirect("user:info_page", id=user_request.id)
    context = {"variant": variant, "questions": questions, "replies": replies, "user_request": user_request}
    return render(request, "user/question.html", context)


def request_page(request, id):
    user_request = UserRequest.objects.get(id=id)
    replies = UserReply.objects.filter(user_request=user_request)
    context = {"user_request": user_request, "replies": replies}
    return render(request, "user/request_page.html", context)


@login_required
def info_page(request, id):
    user_request = UserRequest.objects.get(id=id)
    form = UserRequestInfoForm(
        request.POST or None, instance=user_request, initial={"phone": request.user.phone_number}
    )
    if form.is_valid():
        form.save()
        user_request.is_submitted = True
        user_request.save()
        return redirect("user:request_page", id=user_request.id)
    context = {"form": form, "user_request": user_request}
    return render(request, "user/info_page.html", context)


def handler404(request, exception):
    return render(request, "user/404.html", status=404)


def send_otp(phone_number, otp):
    print(f"OTP: {otp}")


def login_page(request):
    form = PhoneOTPForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.otp = random.randint(100000, 999999)
            data.save()
            send_otp(data.phone_number, data.otp)
            user = (
                User.objects.filter(username=data.phone_number).first()
                if User.objects.filter(username=data.phone_number).exists()
                else User.objects.create_user(username=data.phone_number)
            )
            return redirect("user:verify_page", pk=user.pk)
    return render(request, "user/login.html", context={"form": form})


def verify_page(request, pk):
    user_instance = get_object_or_404(User, pk=pk)
    otp_instance = PhoneOTP.objects.filter(phone_number=user_instance.username).first()
    if request.method == "POST":
        otp = request.POST.get("otp")
        if otp_instance.otp == int(otp):
            user = authenticate(username=user_instance.username, password=otp)
            # TODO: authenticate user here
            print(user)
            if user is not None:
                login(request, user)

            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Invalid OTP")
    return render(request, "user/verify.html", context={"user_instance": user_instance, "otp_instance": otp_instance})


def resend_page(request, pk):
    user_instance = get_object_or_404(User, pk=pk)
    otp_instance = PhoneOTP.objects.filter(phone_number=user_instance.username).first()
    otp_instance.otp = random.randint(100000, 999999)
    otp_instance.save()
    send_otp(otp_instance.phone_number, otp_instance.otp)
    return JsonResponse({"message": "OTP sent successfully"})


def logout_page(request):
    logout(request)
    return redirect("/")
