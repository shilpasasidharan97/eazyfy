import json
import uuid

from main.models import BannerImage, Team
from official.models import Brand
from official.models import BrandModel
from official.models import CustomerProfile
from official.models import CustomerRegistration
from official.models import Variant
from main.models import Offer
from official.models import Question
from official.models import QuestionOption
from official.models import User
from official.models import UserReply
from official.models import UserRequest
from user.mixin import MessageHandler

import pyotp
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


def index(request):
    banners = BannerImage.objects.all()
    offers = Offer.objects.all()
    brands = Brand.objects.all()
    user = request.user
    context = {"is_index": True, "user": user, "banners": banners, "offers": offers, "brands": brands}
    return render(request, "main/index.html", context)


def about(request):
    context = {"is_about": True, "teams": Team.objects.all()}
    return render(request, "main/about.html", context)


def contact(request):
    return render(request, "main/contact.html")


def terms_and_conditions(request):
    return render(request, "main/terms_and_conditions.html")


def sell_phone(request):
    context = {"is_sellphone": True, "brands": Brand.objects.all(), "offers": Offer.objects.all()}
    return render(request, "main/sellphone.html", context)


def buy_phone(request):
    context = {"is_buyphone": True, "brands": Brand.objects.all(), "offers": Offer.objects.all()}
    return render(request, "main/buyphone.html", context)


def repair_phone(request):
    context = {"is_repair": True, "brands": Brand.objects.all(), "offers": Offer.objects.all()}
    return render(request, "main/repairphone.html", context)


def privacy_policy(request):
    return render(request, "main/privacy-policy.html")


def account(request):
    return render(request, "main/account.html")


def payment(request):
    return render(request, "main/payment.html")


def comingsoon(request):
    context = {"is_gadget": True}
    return render(request, "main/comingsoon.html", context)


def find_new_gadget(request):
    context = {"is_newgadget": True}
    return render(request, "main/find_new_gadget.html", context)
