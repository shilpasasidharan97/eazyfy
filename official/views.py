from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def base(request):
    return render(request,'official/partials/base.html')

# login
def loginPage(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        user = authenticate(request,phone_number=phone, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser == True:
                return redirect('official:home')
            elif user.is_franchise == True:
                return redirect('franchise:index')
            elif user.is_pickupboy == True:
                return redirect('pickupboy:index')
            # elif user.is_customer == True:
            #     return redirect('user:about')
            # elif user.Student !=None:
            #     return redirect('student:home')
        else:
            msg = "* Incorrect email or password *"
            return render(request,'official/login.html',{'msg':msg,})
    return render(request,'official/login.html')


# FORGOT PASSWORD
def forgotPassword(request):
    return render(request,'official/forgot_password.html')


@login_required(login_url='/official/loginpage')
def home(request):
    context = {
        "is_index":True
    }
    return render(request,'official/home.html',context)


# franchise listing
@login_required(login_url='/official/loginpage')
def franchise(request):
    if request.method == 'POST':
        name = request.POST['name']
        franchise_id = request.POST['franchise_id']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        photo = request.FILES.get('photo',"not found")
        franchise = Franchise(name=name, franchise_id=franchise_id, email=email, phone=phone, photo=photo, address=address, password=password)
        franchise.save()

        User = get_user_model()
        User.objects.create_user(phone_number=phone, password=password,franchise=franchise, is_franchise=True)
        return redirect('official:franchise')
    else:
        franchise_list = Franchise.objects.all().order_by('name')
        context={
            "is_franchise":True,
            "franchise_list" : franchise_list 
        }
        return render(request,'official/franchise.html',context)


# edit franchise
def EditFranchise(request,id):
    print(id)
    franchise=request.user.franchise
    print(franchise)
    franchise = Franchise.objects.get(id=id)
    context = {
        "is_editprofile": True,
        "franchise":franchise
        }
    return redirect('/official/franchise',context)


@csrf_exempt
def getprofiledata(request,id):
    details = Franchise.objects.get(id=id)
    data = {
        "fid":details.franchise_id,
        "name": details.name,
        "email": details.email,
        "phone": details.phone,
        "address": details.address,
        # "photo": details.photo.url,
    }
    return JsonResponse({"value": data})


@csrf_exempt
def editform(request,id):
    fid = request.POST['fid']
    name = request.POST['fname']
    email = request.POST['femail']
    phone = request.POST['fphone']
    address = request.POST['faddress']
    # photo = request.FILES['fphoto']
    Franchise.objects.filter(id=id).update(franchise_id=fid, name=name, email=email, phone=phone, address=address)
    get_user_model().objects.filter(franchise__id=id).update(phone_number=phone,email=email)
    data ={
        "ss":"csac",
    }
    return JsonResponse(data)


def viewFranchiseDetails(request,id):
    franchise_details = Franchise.objects.get(id=id)
    pickup_boys = PickUpBoy.objects.filter(franchise=franchise_details)
    context ={
        "franchise_details":franchise_details,
        "pickup_boys":pickup_boys,
    }
    return render(request,'official/view_franchise.html',context)


def DeleteFranchise(request,id):
    print("#"*20)
    Franchise.objects.get(id=id).delete()
    return redirect('/official/franchise')


def pickUpBoyList(request,id):
    franchise_details = Franchise.objects.get(id=id)
    return render(request,'official/pickupboy_list.html')


def brand(request):
    brands = Brand.objects.all().order_by('name')
    if request.method == 'POST':
        name = request.POST['name']
        photo = request.FILES['photo']
        new_brand = Brand(name=name, image=photo)
        new_brand.save()
    context = {
        "is_product":True,
        "brands":brands,
    }
    return render(request,'official/brand.html', context)


# edit brand
@csrf_exempt
def getbranddata(request,id):
    print(id)
    details = Brand.objects.get(id=id)
    data = {
        "name": details.name,
        "photo": details.image.url,
        "id":details.id,
    }
    return JsonResponse({"value": data})

# @csrf_exempt
def editBrand(request,id):
    newId = str(id)
    brand_name = request.POST['bname'+newId]
    brand_photo = request.FILES.get("bphoto"+newId,"notfount")
    # print(brand_photo,"$"*10)
    Brand.objects.filter(id=id).update(name=brand_name)
    if brand_photo != "notfount":
        brsnd=Brand.objects.get(id=id)
        brsnd.image=brand_photo
        brsnd.save()
    return redirect('official:brand')


def DeleteBrand(request,id):
    print("#"*20)
    Brand.objects.get(id=id).delete()
    return redirect('/official/brand')


def Model(request,id):
    brand = Brand.objects.get(id=id)
    models = BrandModel.objects.filter(brand=brand)
    if request.method == 'POST':
        brand = brand
        name =request.POST['name']
        image =request.FILES['image']
        
        new_model = BrandModel(brand=brand, image=image, name=name)
        new_model.save()
    context = {
        "models":models,
        "brand":brand
    }
    return render(request,'official/model.html', context)


def getModelData(request,id):
    getmodel = BrandModel.objects.get(id=id)
    # print(getmodel)
    data = {
        # "fkid":getmodel.brand.id,
        "mphoto":getmodel.image.url,
        "mname":getmodel.name
    }
    return JsonResponse(data)


def editModel(request,id):
    print(id)
    new_id = str(id)
    model_name = request.POST['mname'+new_id]
    model_photo = request.FILES.get('mphoto'+new_id, "not found" )
    BrandModel.objects.filter(id=id).update( name=model_name, brand=id)
    if model_photo != 'not found':
        model = BrandModel.objects.get(id=id)
        model.image=model_photo
        model.save()
    else:
        pass
    return redirect('/official/model/'+new_id)


def modelSpecification(request,id):
    brand = BrandModel.objects.get(brand=id)
    models_spec = ModelSpecifications.objects.filter(Brand_model=brand)
    if request.method == 'POST':
        brand = brand
        ram =request.POST['ram']
        internal_storage =request.POST['internal_storage']
        year =request.POST['year']
        color =request.POST['color']
        price = request.POST['price']
        
        new_model = ModelSpecifications(Brand_model=brand, RAM=ram, color=color, internal_storage=internal_storage, year=year, price=price)
        new_model.save()
    context = {
        "models_spec":models_spec,
    }
    return render(request,'official/specification.html', context)


# ALL QUESTION
def questions(request):
    device_type = DeviceType.objects.all()
    context = {
        "is_questions":True,
        "device_type":device_type,
    }
    return render(request,'official/questions.html', context)


# QUESTION ADDING
def questionAdding(request):
    qst = Questions.objects.all().count() 
    qstcount = qst + 1 
    context = {
        "qstcount":qstcount,
    }
    return render(request,'official/questions_adding.html',context)


@csrf_exempt
def questsave(request):
    question_data = request.POST['question']
    qst_type = "Objective"
    device_type = DeviceType.objects.get(device_type="Mobile")
    new_question = Questions(questions=question_data, question_type=qst_type,device_type=device_type)
    new_question.save()
    qst_count = Questions.objects.filter(device_type=device_type).count()
    countt = qst_count + 1
    data = {
        "qstno":countt,
    }
    return JsonResponse(data)


@csrf_exempt
def subquestionFirst(request):
    print("#"*20)
    question = request.POST['qst']
    qst_type = "image_type"
    device_type = DeviceType.objects.get(device_type="Mobile")
    new_question = Questions(questions=question, question_type=qst_type,device_type=device_type)
    new_question.save()
    # qst_count = Questions.objects.filter(device_type=device_type).count()
    qest_pk = new_question.id
    # countt = qst_count + 1
    data = {
        # "qstno":qst_count,
        "qest_pk":qest_pk,
    }
    return JsonResponse(data)


def subquestionPage(request,id):
    question = Questions.objects.get(id=id)
    device_type = DeviceType.objects.get(device_type="Mobile")
    qst_count = Questions.objects.filter(device_type=device_type).count()
    sub_qst = QuestionOption.objects.filter(question=question)
    if request.method == "POST" or request.FILES:
        discription = request.POST['discription']
        image = request.FILES['images']
        new_sub_qst = QuestionOption(question=question,image_upload=image,image_description=discription)
        new_sub_qst.save()
        return redirect('/official/suquestionAddingPage/'+str(question.id))
    context = {
        "question":question,
        "qst_count":qst_count,
        "sub_qst":sub_qst,
    }
    return render(request,'official/sub-question.html',context)


@csrf_exempt
def suquestionAddingData(request):
    print("#"*20)
    print(request.POST)

    question = request.POST['disc']
    qstpk = request.POST['qstpk']
    img = request.POST.get('imgk')
    data = {
        "msg":"msg",
    }
    return JsonResponse(data)


def userRequestList(request):
    context = {
        "is_request":True

    }
    return render(request,'official/user_request.html',context)


def userDetails(request):
    return render(request,'official/view_userdetails.html')


def transactionHistory(request):
    context = {
        "is_transaction":True
    }
    return render(request,'official/transaction_history.html',context)


def wallet(request):
    context = {
        "is_wallet":True
    }
    return render(request,'official/wallet.html',context)


def profile(request):
    return render(request,'official/profile.html')


def logout_view(request):
    logout(request)
    return redirect('/official/loginpage')