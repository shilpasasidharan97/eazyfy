import datetime

from main.models import BannerImage
from main.models import Offer
from user.helpers import payment_mail

from .models import AdminSendRecord
from .models import Brand
from .models import BrandModel
from .models import DeviceType
from .models import Franchise
from .models import FranchiseWallet
from .models import PickUpBoy
from .models import Question
from .models import QuestionOption
from .models import UserRequest
from .models import Variant
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


def user_request_list(request):
    requests = UserRequest.objects.filter(is_submitted=True)
    context = {
        "is_request": True,
        "all_requests": requests,
        "quoted_requests": requests.filter(is_quoted=True),
        "unquoted_requests": requests.filter(is_quoted=False),
    }
    return render(request, "official/user_request.html", context)


def request_details(request, id):
    request_details = UserRequest.objects.get(id=id)
    context = {"is_request": True, "request_details": request_details}
    return render(request, "official/view_userdetails.html", context)


# login
def loginPage(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        password = request.POST["password"]

        user = authenticate(request, phone_number=phone, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("official:home")
            if user.is_franchise:
                return redirect("franchise:index")
            if user.is_pickupboy:
                return redirect("pickupboy:index")
        else:
            msg = "* Incorrect email or password *"
            return render(request, "official/login.html", {"msg": msg})
    return render(request, "official/login.html")


# FORGOT PASSWORD
def forgotPassword(request):
    return render(request, "official/forgot_password.html")


@login_required(login_url="/official/loginpage")
def home(request):
    franchise_count = Franchise.objects.all()
    pickupboy_count = PickUpBoy.objects.all()
    context = {"is_index": True, "franchise_count": franchise_count.count(), "pickupboy_count": pickupboy_count.count()}
    return render(request, "official/home.html", context)


# franchise listing
@login_required(login_url="/official/loginpage")
def franchise(request):
    if request.method == "POST":
        name = request.POST["name"]
        franchise_id = request.POST["franchise_id"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        password = request.POST["password"]
        address = request.POST["address"]
        photo = request.FILES.get("photo", "not found")
        franchise = Franchise(
            name=name,
            franchise_id=franchise_id,
            email=email,
            phone=phone,
            photo=photo,
            address=address,
            password=password,
        )
        franchise.save()

        User = get_user_model()
        User.objects.create_user(phone_number=phone, password=password, franchise=franchise, is_franchise=True)
        wallet = FranchiseWallet(franchise=franchise)
        messages.success(request, "Franchise added successfully")
        wallet.save()
        return redirect("official:franchise")

    franchise_list = Franchise.objects.all().order_by("name")
    context = {"is_franchise": True, "franchise_list": franchise_list}
    return render(request, "official/franchise.html", context)


# edit franchise
def EditFranchise(request, id):
    franchise = request.user.franchise
    franchise = Franchise.objects.get(id=id)
    context = {"is_editprofile": True, "franchise": franchise}
    return redirect("/official/franchise", context)


@csrf_exempt
def getprofiledata(request, id):
    details = Franchise.objects.get(id=id)
    data = {
        "fid": details.franchise_id,
        "name": details.name,
        "email": details.email,
        "phone": details.phone,
        "address": details.address,
        # "photo": details.photo.url,
    }
    return JsonResponse({"value": data})


@csrf_exempt
def editform(request, id):
    fid = request.POST["fid"]
    name = request.POST["fname"]
    email = request.POST["femail"]
    phone = request.POST["fphone"]
    address = request.POST["faddress"]
    Franchise.objects.filter(id=id).update(franchise_id=fid, name=name, email=email, phone=phone, address=address)
    get_user_model().objects.filter(franchise__id=id).update(phone_number=phone, email=email)
    messages.success(request, "Franchise details edited")
    data = {"ss": "csac"}
    return JsonResponse(data)


def viewFranchiseDetails(request, id):
    franchise_details = Franchise.objects.get(id=id)
    pickup_boys = PickUpBoy.objects.filter(franchise=franchise_details)
    wallet = FranchiseWallet.objects.get(franchise=franchise_details)
    context = {
        "franchise_details": franchise_details,
        "pickup_boys": pickup_boys,
        "wallet": wallet,
        "count": pickup_boys.count(),
    }
    return render(request, "official/view_franchise.html", context)


def delete_franchise(request, id):
    Franchise.objects.get(id=id).delete()
    return redirect("/official/franchise")


def pickUpBoyList(request, id):
    franchise_details = Franchise.objects.get(id=id)
    context = {"franchise_details": franchise_details}
    return render(request, "official/pickupboy_list.html", context)


def transactionHistory(request):
    transactions = AdminSendRecord.objects.all()
    context = {"is_transaction": True, "transactions": transactions}
    return render(request, "official/transaction_history.html", context)


# WALLET HISTORY
def wallet(request):
    payment_to_franchise = AdminSendRecord.objects.all()
    context = {"is_wallet": True, "payment_to_franchise": payment_to_franchise}
    return render(request, "official/wallet.html", context)


# WALLET_FRANCHISE_LIST AND STATUS
def franchise_wallet(request):
    all_franchise = FranchiseWallet.objects.all()
    context = {"is_wallet": True, "franchise": all_franchise}
    return render(request, "official/wallet_franchise.html", context)


def viewPayment(request, id):
    details = FranchiseWallet.objects.get(id=id)
    data = {"id": details.franchise.id, "franchise_id": details.franchise.franchise_id, "name": details.franchise.name}
    return JsonResponse({"value": data})


@csrf_exempt
def save_payment(request, id):
    now = datetime.datetime.now()
    paid_amount = request.POST["amount"]
    franchise_obj = Franchise.objects.get(id=id)
    franchisewallet = FranchiseWallet.objects.get(franchise=franchise_obj)
    franchise_balance = franchisewallet.wallet_amount
    balance_amount = float(paid_amount) + float(franchise_balance)
    franchise_amount = FranchiseWallet.objects.filter(franchise_id=id).update(
        last_paid_amount=paid_amount, date=now, wallet_amount=balance_amount
    )
    record = AdminSendRecord(franchise=franchise_obj, amount=paid_amount, date=now)
    messages.success(request, "success")
    payment_mail(franchisewallet.id)
    record.save()
    data = {"sss": "sss", "franchise_amount": franchise_amount}
    return JsonResponse(data)


def profile(request):
    return render(request, "official/profile.html")


def logout_view(request):
    logout(request)
    return redirect("/official/loginpage")


def settings(request):
    offerImage = Offer.objects.all()
    bannerImage = BannerImage.objects.all()
    if request.method == "POST":
        banner = request.FILES.get("banner")
        bannerObject = BannerImage(banner=banner)
        bannerObject.save()
    context = {"bannerImage": bannerImage, "offerImage": offerImage}

    return render(request, "official/settings.html", context)


def delete_banner(request, id):
    BannerImage.objects.get(id=id).delete()
    return redirect("/official/settings")


def offers(request):
    if request.method == "POST":
        offer = request.FILES.get("offers")
        phoneOffer = Offer(offer=offer)
        phoneOffer.save()
    return redirect("/official/settings")


def delete_offer(request, id):
    Offer.objects.get(id=id).delete()
    return redirect("/official/settings")
