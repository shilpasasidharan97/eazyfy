from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request,"user/partials/base.html") 

def index(request):
    return render(request,"user/index.html") 