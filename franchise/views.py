from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from official.models import *

# Create your views here.

def index(request):
    return render(request,"franchise/index.html")


@login_required(login_url='/official/loginpage')
def add_pickupboy(request):
    franchise = request.user.franchise
    print(franchise,"#"*20)
    pickup_boys = PickUpBoy.objects.filter(franchise=franchise)
    if request.method == 'POST':
        
        name = request.POST['name']
        pickup_boy_id = request.POST['pickup_boy_id']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        place = request.POST['place']
        address = request.POST['address']
        photo = request.FILES['photo']
        # franchise = franchise
        
        pickup_boy = PickUpBoy(franchise=franchise, pickup_id=pickup_boy_id, name=name, email=email, phone=phone, photo=photo, place=place, address=address, password=password)
        pickup_boy.save()

        User = get_user_model()
        User.objects.create_user(phone_number=phone, password=password,pickup_boy=pickup_boy, is_pickupboy=True)
        return render(request,'franchise/add-pickupboy.html')
    else:
        pickup_boy_list = PickUpBoy.objects.all().order_by('name')
        context={
            "pickup_boy_list" : pickup_boy_list
        }
    context = {
        "pickup_boys":pickup_boys
    }
    return render(request,"franchise/add-pickupboy.html", context)

def profile(request):
    return render(request,"franchise/profile.html")

def order(request):
    return render(request,"franchise/order.html")