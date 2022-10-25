from django.shortcuts import render

# Create your views here.

def base(request):
    return render(request,'official/partials/base.html')

def loginPage(request):
    return render(request,'official/login.html')


def forgotPassword(request):
    return render(request,'official/forgot_password.html')


def home(request):
    return render(request,'official/home.html')


def franchise(request):
    return render(request,'official/franchise.html')


def viewFranchiseDetails(request):
    return render(request,'official/view_franchise.html')


def pickUpBoyList(request):
    return render(request,'official/pickupboy_list.html')


def brand(request):
    return render(request,'official/brand.html')


def Model(request):
    return render(request,'official/model.html')


def modelSpecification(request):
    return render(request,'official/specification.html')


def questionAdding(request):
    return render(request,'official/questions_adding.html')


def userRequestList(request):
    return render(request,'official/user_request.html')


def userDetails(request):
    return render(request,'official/view_userdetails.html')


def transactionHistory(request):
    return render(request,'official/transaction_history.html')


def wallet(request):
    return render(request,'official/wallet.html')