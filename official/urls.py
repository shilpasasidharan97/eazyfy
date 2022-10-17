from django.urls import path
from . import views

app_name = 'official'

urlpatterns = [
    path('loginpage',views.loginPage,name='loginpage'),
    path('forgotpassword',views.forgotPassword,name='forgotpassword'),
    
    path('home',views.home,name='home'),
    path('franchise',views.franchise,name='franchise'),
    path('franchisedetails',views.viewFranchiseDetails,name='franchisedetails'),
    path('brand',views.brand,name='brand'),
    path('model',views.Model,name='model'),
    path('addmodel',views.addModel,name='addmodel'),
     
]