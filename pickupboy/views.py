from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"pickup-boy/index.html")

def total_order(request):
    return render(request,"pickup-boy/total-order.html")

def product_validation(request):
    return render(request,"pickup-boy/product-validation.html")

def product_details(request):
    return render(request,"pickup-boy/product-details.html")

