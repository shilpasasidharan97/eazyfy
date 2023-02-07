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


def login_page(request):
    form = PhoneOTPForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")
            country_code = form.cleaned_data.get("country_code")
            username = f"{country_code}{phone_number}"
            user = (
                User.objects.filter(username=username).first()
                if User.objects.filter(username=username).exists()
                else User.objects.create_user(username=username)
            )
            print(user)

    return render(request, "user/login.html", context={"form": form})


def logout_page(request):
    pass


def register_page(request):
    pass


def verify_page(request):
    pass


def resend_page(request):
    pass
