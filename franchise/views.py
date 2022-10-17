from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request,"franchise/index.html")

def add_pickupboy(request):
    return render(request,"franchise/add-pickupboy.html")

def order(request):
    return render(request,"franchise/order.html")