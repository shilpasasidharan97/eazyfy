import datetime

from user.helpers import payment_mail

from .models import AdminSendRecord
from .models import BannerImage
from .models import Brand
from .models import BrandModel
from .models import DeviceType
from .models import Franchise
from .models import FranchiseWallet
from .models import ModelSpecifications
from .models import Offer
from .models import PickUpBoy
from .models import Question
from .models import QuestionOption
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


def base(request):
    return render(request, "official/partials/base.html")


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
            # elif user.is_customer:
            #     return redirect('user:about')
            # elif user.Student !=None:
            #     return redirect('student:home')
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
        franchise = Franchise(name=name, franchise_id=franchise_id, email=email, phone=phone, photo=photo, address=address, password=password)
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
    context = {"franchise_details": franchise_details, "pickup_boys": pickup_boys, "wallet": wallet, "count": pickup_boys.count()}
    return render(request, "official/view_franchise.html", context)


def DeleteFranchise(request, id):
    Franchise.objects.get(id=id).delete()
    return redirect("/official/franchise")


def pickUpBoyList(request, id):
    franchise_details = Franchise.objects.get(id=id)
    context = {"franchise_details": franchise_details}
    return render(request, "official/pickupboy_list.html", context)


def brand(request):
    brands = Brand.objects.all().order_by("name")
    if request.method == "POST":
        name = request.POST["name"]
        photo = request.FILES["photo"]
        new_brand = Brand(name=name, image=photo)
        messages.success(request, "Brand added successfull ..please complete the spec adding procedure")
        new_brand.save()
    context = {"is_product": True, "brands": brands}
    return render(request, "official/brand.html", context)


# edit brand
@csrf_exempt
def getbranddata(request, id):
    details = Brand.objects.get(id=id)
    data = {"name": details.name, "photo": details.image.url, "id": details.id}
    return JsonResponse({"value": data})


# @csrf_exempt
def editBrand(request, id):
    newId = str(id)
    brand_name = request.POST["bname" + newId]
    brand_photo = request.FILES.get("bphoto" + newId, "notfount")
    Brand.objects.filter(id=id).update(name=brand_name)
    if brand_photo != "notfount":
        brsnd = Brand.objects.get(id=id)
        brsnd.image = brand_photo
        brsnd.save()
    return redirect("official:brand")


def DeleteBrand(request, id):
    Brand.objects.get(id=id).delete()
    return redirect("/official/brand")


def Model(request, id):
    brand = Brand.objects.get(id=id)
    models = BrandModel.objects.filter(brand=brand)
    if request.method == "POST":
        name = request.POST["name"]
        image = request.FILES["image"]

        new_model = BrandModel(brand=brand, image=image, name=name)
        new_model.save()
    context = {"models": models, "brand": brand}
    return render(request, "official/model.html", context)


def getModelData(request, id):
    getmodel = BrandModel.objects.get(id=id)
    data = {
        # "fkid":getmodel.brand.id,
        "mphoto": getmodel.image.url,
        "mname": getmodel.name,
    }
    return JsonResponse(data)


def editModel(request, id):
    new_id = str(id)
    model_name = request.POST["mname" + new_id]
    model_photo = request.FILES.get("mphoto" + new_id, "not found")
    BrandModel.objects.filter(id=id).update(name=model_name, brand=id)
    if model_photo != "not found":
        model = BrandModel.objects.get(id=id)
        model.image = model_photo
        model.save()
    else:
        pass
    return redirect("/official/model/" + new_id)


# modelspecification adding
def modelSpecification(request, id):
    brand = BrandModel.objects.get(brand__id=id)
    models_spec = ModelSpecifications.objects.filter(brand_model=brand)
    if request.method == "POST":
        ram = request.POST["ram"]
        internal_storage = request.POST["internal_storage"]
        year = request.POST["year"]
        color = request.POST["color"]
        price = request.POST["price"]

        new_model = ModelSpecifications(brand_model=brand, RAM=ram, color=color, internal_storage=internal_storage, year=year, price=price)
        new_model.save()
    context = {"models_spec": models_spec}
    return render(request, "official/specification.html", context)


# ALL QUESTION
def questions(request):
    question = Question.objects.all()
    subQuestion = QuestionOption.objects.all()
    image = QuestionOption.objects.filter(question__question_type="image")
    object_type = Question.objects.filter(question_type="Objective")
    device_type = DeviceType.objects.all()
    context = {
        "is_questions": True,
        "device_type": device_type,
        "question": question,
        "objective_count": question.count(),
        "subQuestion_count": subQuestion.count(),
        "subQuestion": subQuestion,
        "image": image,
        "image_count": image.count(),
        "object_type": object_type,
        "object_type_count": object_type.count(),
    }
    return render(request, "official/questions.html", context)


# QUESTION ADDING
def questionAdding(request):
    models = BrandModel.objects.all()
    qst = Question.objects.all().count()
    qstcount = qst + 1

    context = {"qstcount": qstcount, "models": models}
    return render(request, "official/questions_adding.html", context)


@csrf_exempt
def questsave(request):
    question = request.POST["qst"]
    qst_type = "Objective"
    device_type = DeviceType.objects.get(device_type="Mobile")
    new_question = Question(question=question, question_type=qst_type)
    new_question.save()
    qst_count = Question.objects.filter().count()
    countt = qst_count + 1
    data = {"qstno": countt}
    return JsonResponse(data)


@csrf_exempt
def subquestionFirst(request):
    question = request.POST["qst"]
    qst_type = "image"
    device_type = DeviceType.objects.get(device_type="Mobile")
    new_question = Question(question=question, question_type=qst_type)
    new_question.save()
    qest_pk = new_question.id
    data = {
        # "qstno":qst_count,
        "qest_pk": qest_pk
    }
    return JsonResponse(data)


def subquestionPage(request, id):
    question = Question.objects.get(id=id)
    device_type = DeviceType.objects.get(device_type="Mobile")
    qst_count = Question.objects.filter().count()
    sub_qst = QuestionOption.objects.filter(question=question)
    if request.method == "POST" or request.FILES:
        description = request.POST["description"]
        image = request.FILES["images"]
        new_sub_qst = QuestionOption(question=question, image=image, text=description)
        new_sub_qst.save()
        return redirect("/official/suquestionAddingPage/" + str(question.id))
    context = {"question": question, "qst_count": qst_count, "sub_qst": sub_qst, "device_type": device_type}
    return render(request, "official/sub-question.html", context)


@csrf_exempt
def suquestionAddingData(request):
    request.POST.get("imgk")
    data = {"msg": "msg"}
    return JsonResponse(data)


# deduction Amount setting
def deductionSettings(request):
    all_barnd = BrandModel.objects.all()
    context = {"models": all_barnd}
    return render(request, "official/deduction.html", context)


def questionForDeduction(request, id):
    all_questions = QuestionOption.objects.all()
    brandmodel = BrandModel.objects.get(id=id)

    questions = Question.objects.all()
    context = {"all_questions": all_questions, "questions": questions, "brandmodel": brandmodel}
    return render(request, "official/questionfor_deduction.html", context)


def questionId(request):
    quset = request.GET["qstid"]
    question = Question.objects.get(id=quset)
    question_type = question.question_type
    data = []
    if question_type == "image":
        qust_type = {"type": "image"}
        data.append(qust_type)
        question_option = QuestionOption.objects.filter(question__question_type="image", question=question)

        for i in question_option:
            data1 = {"text": i.text, "text_id": i.id, "image": i.image.url}
            data.append(data1)
        return JsonResponse(data, safe=False)
    qust_type = {"type": "Objective"}
    data.append(qust_type)
    return JsonResponse(data, safe=False)


def test(request):
    return render(request, "official/test.html")


def userRequestList(request):
    context = {"is_request": True}
    return render(request, "official/user_request.html", context)


def userDetails(request):
    return render(request, "official/view_userdetails.html")


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
def franchiseWallet(request):
    all_franchise = FranchiseWallet.objects.all()
    context = {"is_wallet": True, "franchise": all_franchise}
    return render(request, "official/wallet_franchise.html", context)


def viewPayment(request, id):
    details = FranchiseWallet.objects.get(id=id)
    data = {"id": details.franchise.id, "franchise_id": details.franchise.franchise_id, "name": details.franchise.name}
    return JsonResponse({"value": data})


@csrf_exempt
def savePayment(request, id):
    now = datetime.datetime.now()
    paid_amount = request.POST["amount"]
    franchise_obj = Franchise.objects.get(id=id)
    franchisewallet = FranchiseWallet.objects.get(franchise=franchise_obj)
    franchise_balance = franchisewallet.wallet_amount
    balance_amount = float(paid_amount) + float(franchise_balance)
    franchise_amount = FranchiseWallet.objects.filter(franchise_id=id).update(last_paid_amount=paid_amount, date=now, wallet_amount=balance_amount)
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


def DeleteBanner(request, id):
    BannerImage.objects.get(id=id).delete()
    return redirect("/official/settings")


def offers(request):
    if request.method == "POST":
        offer = request.FILES.get("offers")
        phoneOffer = Offer(offer=offer)
        phoneOffer.save()
    return redirect("/official/settings")


def DeleteOffer(request, id):
    Offer.objects.get(id=id).delete()
    return redirect("/official/settings")
