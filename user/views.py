from official.models import Question
from official.models import QuestionOption
from official.models import User
from official.models import UserReply
from official.models import UserRequest
from official.models import Variant, Customer

from .forms import UserRequestInfoForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


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


def customer_login(request):
    if request.method == "POST":
        countryCode = request.POST["countryCode"]
        number = request.POST["number"]
        login_countryCode = countryCode + number
        password = request.POST["password"]
        user = authenticate(request, phone_number=login_countryCode, password=password)
        if user is not None:
            login(request, user)
            if user.is_customer:
                return redirect("main:index")
            return redirect("auth_login")
        return redirect("auth_login")
    else:
        return render(request, "user/login.html")


@csrf_exempt
def check_phone_number(request):
    phone = request.POST["phone"]
    if User.objects.filter(phone_number=phone).exists():
        data = {"status": 1, "msg": "User Alreay Exists in the same phone number"}
        return JsonResponse(data)
    data = {"msg": '"user not exists', "status": 0}
    return JsonResponse(data)


# def otp_fun(request, id):
#     profile = CustomerProfile.objects.get(test_id=id)
#     totp = pyotp.TOTP(profile.auth_token, interval=300)
#     otp = totp.now()
#     OtpModel(otp=otp).save()
#     if request.method == "POST":
#         enter_otp = request.POST["otp"]
#         verification = totp.verify(enter_otp)
#         if verification:
#             return redirect("main:login")
#     send_message(otp, profile.user.phone_number)
#     return render(request, "user/otp_generation.html", {"token": profile.test_id})


# def forgot(request):
#     if request.method == "POST":
#         email = request.POST["email"]
#         if not User.objects.filter(email=email).first():
#             messages.success(request, "Not user found with this email.")
#             return redirect("/forgot")
#         user_obj = User.objects.get(email=email)
#         token = str(uuid.uuid4())
#         profile_obj = CustomerProfile.objects.get(user=user_obj)
#         profile_obj.forget_password_token = token
#         profile_obj.save()
#         send_forget_password_mail(user_obj.email, token)
#         messages.success(request, "An email is sent.")
#         return redirect("/forgot")
#     return render(request, "user/forgot.html")


# def reset_password(request, token):
#     profile_obj = CustomerProfile.objects.filter(forget_password_token=token).first()
#     context = {"user_id": profile_obj.user.id}
#     if request.method == "POST":
#         new_password = request.POST["password"]
#         user_id = request.POST.get("user_id")
#         if user_id is None:
#             messages.warning(request, "No user id found.")

#             return redirect(f"/change-password/{token}/")
#         user_obj = User.objects.get(id=user_id)
#         user_obj.set_password(new_password)
#         user_obj.save()
#         messages.success(request, "An email sent")
#         return redirect(f"/change-password/{token}/")
#     return render(request, "user/reset_password.html", context)


# def resend_otp(request, token):
#     user = CustomerProfile.objects.filter(test_id=token).last()
#     user_secret_key = pyotp.random_base32()
#     user.auth_token = user_secret_key
#     user.save()
#     return redirect(f"/otp-page/{user.test_id}")


def handler404(request, exception):
    return render(request, "user/404.html", status=404)


def user_logout(request):
    logout(request)
    return redirect("main:index")
