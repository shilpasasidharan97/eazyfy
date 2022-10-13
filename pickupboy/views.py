from django.shortcuts import render

# Create your views here.

def base(request):
    return render(request,"pickup-boy/partials/base.html")

def index(request):
    return render(request,"pickup-boy/index.html")

def total_order(request):
    return render(request,"pickup-boy/total-order.html")

def customer_selfy(request):
    return render(request,"pickup-boy/customer-selfy.html")

def product_details(request):
    return render(request,"pickup-boy/product-details.html")

def verification_questions(request):
    return render(request,"pickup-boy/verification-questions.html")

def complete(request):
    return render(request,"pickup-boy/complete.html")

def fail(request):
    return render(request,"pickup-boy/fail.html")

def requote(request):
    return render(request,"pickup-boy/requote.html")