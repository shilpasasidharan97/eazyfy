import datetime

from main.models import BannerImage
from main.models import Offer
from user.helpers import payment_mail

from .forms import AddAmountForm
from .forms import FranchiseAssignForm
from .models import Franchise
from .models import FranchiseWallet
from .models import PickUpBoy
from .models import PickupData
from .models import UserRequest
from django.conf import settings
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


@login_required
def user_request_list(request):
    requests = UserRequest.objects.filter(is_submitted=True)
    assigned_to_franchise_requests = requests.filter(is_assigned_to_franchise=True)
    unassigned_to_franchise_requests = requests.filter(is_assigned_to_franchise=False)
    assigned_to_pickup_requests = requests.filter(is_assigned_to_pickup=True)
    quoted_requests = requests.filter(is_quoted=True)
    context = {
        "is_request": True,
        "all_requests": requests,
        "assigned_to_franchise_requests": assigned_to_franchise_requests,
        "unassigned_to_franchise_requests": unassigned_to_franchise_requests,
        "assigned_to_pickup_requests": assigned_to_pickup_requests,
        "quoted_requests": quoted_requests,
    }
    return render(request, "official/user_request.html", context)


@login_required
def request_details(request, id):
    request_details = UserRequest.objects.get(id=id)
    pickup_data, _ = PickupData.objects.get_or_create(user_request=request_details)
    form = FranchiseAssignForm(request.POST or None, instance=request_details)
    if request.method == "POST":
        if form.is_valid():
            data = form.save()
            data.is_assigned_to_franchise = True
            data.save()
            messages.success(request, "Request Assigned Successfully")
            return redirect("official:userrequestlist")
    context = {"is_request": True, "request_details": request_details, "form": form, "pickup_data": pickup_data}
    return render(request, "official/order_details.html", context)


# login
def loginPage(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        password = request.POST["password"]

        user = authenticate(request, phone_number=phone, password=password)
        print(user)
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


@login_required
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


@login_required
def viewFranchiseDetails(request, id):
    franchise = Franchise.objects.get(id=id)
    pickup_boys = PickUpBoy.objects.filter(franchise=franchise)
    wallet = FranchiseWallet.objects.filter(franchise=franchise)
    context = {
        "franchise_details": franchise,
        "pickup_boys": pickup_boys,
        "wallet": wallet,
        "count": pickup_boys.count(),
    }
    return render(request, "official/view_franchise.html", context)


@login_required
def delete_franchise(request, id):
    Franchise.objects.get(id=id).delete()
    return redirect("/official/franchise")


@login_required
def pickUpBoyList(request, id):
    franchise = Franchise.objects.get(id=id)
    context = {"franchise_details": franchise}
    return render(request, "official/pickupboy_list.html", context)


@login_required
def transactionHistory(request):
    transactions = FranchiseWallet.objects.all()
    context = {"is_transaction": True, "transactions": transactions}
    return render(request, "official/transaction_history.html", context)


@login_required
def wallet(request):
    transactions = FranchiseWallet.objects.all()
    admin_transactions = transactions.filter(type="to_franchise")
    franchise_transactions = transactions.filter(type="to_admin")
    admin_transactions_sum = sum(w.amount for w in admin_transactions)
    franchise_transactions_sum = sum(w.amount for w in franchise_transactions)
    admin_wallet_amount = int(settings.ADMIN_WALLET_AMOUNT) - admin_transactions_sum + franchise_transactions_sum
    context = {
        "is_wallet": True,
        "transactions": transactions,
        "admin_wallet_amount": admin_wallet_amount,
        "admin_transactions": admin_transactions,
        "franchise_transactions": franchise_transactions,
    }
    return render(request, "official/wallet.html", context)


@login_required
def franchise_wallet(request):
    franchises = Franchise.objects.all()
    form = AddAmountForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.type = "to_franchise"
            data.save()
            return redirect("official:franchisewallet")
    context = {"is_wallet": True, "franchises": franchises, "form": form}
    return render(request, "official/wallet_franchise.html", context)


@login_required
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
    franchise_amount = FranchiseWallet.objects.filter(franchise_id=id).update(date=now, wallet_amount=balance_amount)
    messages.success(request, "success")
    payment_mail(franchisewallet.id)
    data = {"sss": "sss", "franchise_amount": franchise_amount}
    return JsonResponse(data)


@login_required
def profile(request):
    return render(request, "official/profile.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("/official/loginpage")


@login_required
def official_settings(request):
    offerImage = Offer.objects.all()
    bannerImage = BannerImage.objects.all()
    if request.method == "POST":
        banner = request.FILES.get("banner")
        bannerObject = BannerImage(banner=banner)
        bannerObject.save()
    context = {"bannerImage": bannerImage, "offerImage": offerImage}
    return render(request, "official/settings.html", context)


@login_required
def delete_banner(request, id):
    BannerImage.objects.get(id=id).delete()
    return redirect("/official/settings")


@login_required
def offers(request):
    if request.method == "POST":
        offer = request.FILES.get("offers")
        phoneOffer = Offer(offer=offer)
        phoneOffer.save()
    return redirect("/official/settings")


@login_required
def delete_offer(request, id):
    Offer.objects.get(id=id).delete()
    return redirect("/official/settings")
