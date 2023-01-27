from main.models import BannerImage
from main.models import Offer
from main.models import Team
from official.models import Brand

from django.shortcuts import render


def index(request):
    banners = BannerImage.objects.all()
    offers = Offer.objects.all()
    user = request.user
    context = {"is_index": True, "user": user, "banners": banners, "offers": offers}
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


def comingsoon(request):
    context = {"is_gadget": True}
    return render(request, "main/comingsoon.html", context)


def find_new_gadget(request):
    context = {"is_newgadget": True}
    return render(request, "main/find_new_gadget.html", context)
